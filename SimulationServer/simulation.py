from car import Car
from config import SimulationConfig
from idm import idm
import json
from stopwave import StopWave
from time import sleep, time
from datetime import datetime
from valkey import Valkey
import random


class Simulation:
    def __init__(self, valkey: Valkey) -> None:
        self._id = 0
        self.valkey = valkey
        self.head: Car = None
        self.tail: Car = None

        self.config = SimulationConfig()
        self.config.read(valkey)

        self.stopwaves: list[StopWave] = []
        self.is_collecting_data = False
        self.collected_samples = 0
        self.data: dict[dict] = {}

        self.create_car()

    def main_loop(self) -> None:
        config_refresh_time = time()
        while True:
            if time() - config_refresh_time > 1:
                reset = self.valkey.get("reset")
                reset = int(reset.decode()) if reset is not None else 0
                if reset:
                    self.clear()
                    self.populate()
                    self.valkey.set("reset", 0)

                collect_data = self.valkey.get("collect_data")
                collect_data = int(collect_data.decode()) if collect_data is not None else 0
                if collect_data and not self.is_collecting_data:
                    self.start_data_collection()
                self.config.read(self.valkey)
                config_refresh_time = time()
            start_time = time()
            self.update_cars()
            self.valkey.set("cars", self.serialize_cars())

            if self.is_collecting_data:
                if self.collected_samples == self.config.data_collection_brake_offset:
                    car = self.get_car_by_id(self.config.data_collection_braking_car_id)
                    car.brake_amount = self.config.data_collection_brake_pressure

                if self.collected_samples == self.config.data_collection_brake_samples\
                        + self.config.data_collection_brake_offset:
                    car = self.get_car_by_id(self.config.data_collection_braking_car_id)
                    car.brake_amount = 0

                if self.collected_samples >= self.config.data_collection_samples:
                    self.stop_data_collection()
                else:
                    self.collect_data()

            elapsed_time = time() - start_time
            if self.config.real_time:
                sleep(self.config.update_interval - elapsed_time)

    def update_cars(self) -> None:
        hw1_car = self.valkey.get("hw1_car")
        hw2_car = self.valkey.get("hw2_car")
        hw1_car = int(hw1_car.decode()) if hw1_car else None
        hw2_car = int(hw2_car.decode()) if hw2_car else None

        self.stopwaves = []
        car = self.head
        while car:
            if car.speed > self.config.stop_wave_speed:
                car = car.prev
                continue
            if not car.next:
                car = car.prev
                continue
            if not car.is_smart:
                car = car.prev
                continue
            self.stopwaves.append(StopWave.from_start(car, self.config.stop_wave_speed))
            car = self.stopwaves[-1].stop.prev

        car = self.head
        while car:
            if car.position >= self.config.kill_distance:
                self.destroy_car(car)
                car = car.prev
                continue

            if not self.is_collecting_data:
                if car.id == hw1_car:
                    car.hw1_target = True
                    hw1_brake = self.valkey.get("hw1_brake")
                    car.brake_amount = int(hw1_brake.decode()) if hw1_brake else 0
                else:
                    car.hw1_target = False

                if car.id == hw2_car:
                    car.hw2_target = True
                    hw2_brake = self.valkey.get("hw2_brake")
                    car.brake_amount = int(hw2_brake.decode()) if hw2_brake else 0
                else:
                    car.hw2_target = False

                if car.id not in (hw1_car, hw2_car):
                    car.brake_amount = 0

            self.update_car(car)
            if car.id == hw1_car:
                self.valkey.set("hw1_rec_speed", int(car.recommended_speed))
                self.valkey.set("hw1_speed", int(car.speed))
            if car.id == hw2_car:
                self.valkey.set("hw2_rec_speed", int(car.recommended_speed))
                self.valkey.set("hw2_speed", int(car.speed))

            car = car.prev

        v = self.config.speed_limit
        dynamic_term = (v * (v - max(self.tail.speed, 10))) / (2 * self.config.braking_factor)
        s_star = self.config.car_length + self.config.target_distance + \
            max(0, v * self.config.time_headway + dynamic_term)
        if self.tail.position + self.config.car_length > s_star:
            # print(f"V is {v}, self.tail.speed is {self.tail.speed}, s_star is {s_star}. Dynamic tem is {dynamic_term}")
            self.create_car()
            # Offset because we don't have infinite updates / sec
            self.tail.position = max(0, s_star - self.tail.next.position - self.config.car_length)

        self.valkey.set("head", self.head.id)
        self.valkey.set("tail", self.tail.id)

    def update_car(self, car: Car) -> None:
        if car.brake_amount:
            # Decrease reference speed by brake_amount, but not below 0
            # car.reference_speed = max(0.1, car.reference_speed - car.brake_amount)
            # car.accel = 1 - (car.brake_amount / 255)
            acceleration = car.brake_amount / 255 * 60 * self.config.update_interval
            car.speed = max(0, car.speed - acceleration)

        else:
            # Gradually restore reference speed up to original speed

            # if car.reference_speed < car.target_speed:
            #     car.reference_speed = min(
            #         self.config.initial_speed, car.target_speed + car.max_ref_inc
            #     )

            car.accel = idm(car, self.config)
            # car.accel = pid_calculator(car, self.config)

            car.speed += car.accel * self.config.update_interval
            # car.speed = min(car.speed, car.target_speed)
            car.speed = max(0, car.speed)

        car.in_stopwave = False
        car.detected_stopwave = None
        for wave in self.stopwaves:  # Stopwaves are ordered where first is closest to end of the road
            if wave.in_range(car):
                car.detected_stopwave = wave  # Last one is the nearest
            if car in wave:
                car.in_stopwave = True

        car.position += car.speed * self.config.update_interval

        if car.is_smart:
            car.time_headway = self.config.time_headway
            car.recommended_speed = self.get_recommended_speed(car)
        else:
            car.recommended_speed = self.config.speed_limit
            car.time_headway = self.config.time_headway

    def get_recommended_headway(self, car: Car) -> int:
        if car.in_stopwave:
            return self.config.time_headway

        if not car.detected_stopwave:
            return self.config.time_headway

        return self.config.time_headway * self.config.headway_factor

    def get_recommended_speed(self, car: Car) -> int:
        if car.in_stopwave:
            return self.config.speed_limit

        if not car.detected_stopwave:
            return self.config.speed_limit

        distance_to_car_in_front = car.next.position - car.position

        recommended_speed = distance_to_car_in_front / (self.config.time_headway * self.config.headway_factor)

        return recommended_speed

    def get_car_by_id(self, car_id: int) -> Car | None:
        car = self.head
        while car:
            if car.id == car_id:
                return car
            car = car.prev
        return None

    def serialize_cars(self) -> bytes:
        rep = bytes()
        car = self.head
        while car:
            rep += bytes(car)
            car = car.prev
        return rep

    def create_car(self) -> Car:
        car = Car(config=self.config, id=self._id)
        self._id += 1
        if not self.head:
            self.head = car

        car.next = self.tail
        self.tail = car

        if random.random() < self.config.adoption_rate:
            car.is_smart = True

    def destroy_car(self, car: Car) -> None:
        if car.prev:
            car.prev.next = car.next
        if car.next:
            car.next.prev = car.prev
        if car is self.head:
            self.head = car.prev
        if car is self.tail:
            self.tail = car.next
        del car

    def clear(self) -> None:
        car = self.head
        self.head = self.tail = None
        while car:
            next_car = car.prev
            del car
            car = next_car
        self._id = 0

    def populate(self) -> None:
        self.create_car()
        spawn_position = self.config.kill_distance
        self.tail.position = spawn_position

        s_star = self.config.car_length + self.config.target_distance + \
            max(0, self.config.speed_limit * self.config.time_headway)
        spawn_position -= s_star

        while spawn_position >= 0:
            self.create_car()
            self.tail.position = spawn_position
            spawn_position -= s_star

    def start_data_collection(self) -> None:
        self.clear()
        self.populate()
        self.data = {
            i: {
                "id": i,
                "position": [],
                "speed": [],
                "accel": [],
                "gap": [],
            }
            for i in range(
                self.config.data_collection_braking_car_id,
                self.config.data_collection_braking_car_id +
                self.config.data_collection_count*self.config.data_collection_step,
                self.config.data_collection_step
            )
        }
        self.is_collecting_data = True
        self.valkey.set("collect_data", 0)
        car = self.get_car_by_id(self.config.data_collection_braking_car_id)
        car.brake_amount = 0
        car.hw1_target = True
        car.hw2_target = True

    def stop_data_collection(self) -> None:
        self.is_collecting_data = False
        # from os.path import exists
        # name = 1

        # while exists(f"data_{name:.1f}.json"):
        #     name += 0.1
        # with open(f"data_{name:.1f}.json", "w") as f:
        #     json.dump(self.data, f)
        file_name = f"data_{datetime.now().strftime('%d-%m_%H:%M:%S')}.json"
        with open(file_name, "w") as f:
            json.dump(self.data, f)
        self.collected_samples = 0

    def collect_data(self) -> None:
        print(f"Collecting data: {((self.collected_samples+1)/self.config.data_collection_samples)*100:2f}%")
        target_ids = set(range(
            self.config.data_collection_braking_car_id,
            self.config.data_collection_braking_car_id +
            self.config.data_collection_count*self.config.data_collection_step,
            self.config.data_collection_step
        ))
        car = self.head
        while car:
            if car.id not in target_ids:
                car = car.prev
                continue
            self.data[car.id]["position"].append(car.position)
            self.data[car.id]["speed"].append(car.speed)
            self.data[car.id]["accel"].append(car.accel)
            self.data[car.id]["gap"].append(car.next.position - car.position)
            target_ids.discard(car.id)
            car = car.prev

        self.collected_samples += 1


def main():
    valkey = Valkey(host="localhost", port=6379, db=0)
    sim = Simulation(valkey)
    print(sim.config.__dict__)


if __name__ == "__main__":
    main()
