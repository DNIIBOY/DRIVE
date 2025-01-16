from car import Car
from config import SimulationConfig
from idm import idm
import json
from stopwave import StopWave
from time import sleep, time
from datetime import datetime
from valkey import Valkey
import random


def get_val(key: str, valkey: Valkey, default=0) -> int:
    val = valkey.get(key)
    return int(val.decode()) if val is not None else default


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
        self.brake_wave = False

        self.collected_samples = 0
        self.brake_wave_samples = 0

        self.data: dict[dict] = {}

        self.is_monte_carlo = False
        self.monte_carlo_step = 0

        self.create_car()

    def main_loop(self) -> None:
        config_refresh_time = time()
        while True:
            if time() - config_refresh_time > 1:
                self.read_config()
                config_refresh_time = time()

            start_time = time()
            self.update_cars()
            self.valkey.set("cars", self.serialize_cars())

            if self.brake_wave:
                self.update_brake_wave()

            if self.is_collecting_data:
                if self.collected_samples >= self.config.data_collection_samples:
                    self.stop_data_collection()
                else:
                    self.collect_data()

            if self.config.real_time:
                elapsed_time = time() - start_time
                diff = self.config.update_interval - elapsed_time
                if diff >= 0:
                    sleep(diff)
                else:
                    print("Warning: Update interval exceeded")

    def update_cars(self) -> None:
        hw1_car = get_val("hw1_car", self.valkey, None)
        hw2_car = get_val("hw2_car", self.valkey, None)

        self.detect_stopwaves()
        car = self.head
        while car:
            if car.position >= self.config.kill_distance:
                self.destroy_car(car)
                car = car.prev
                continue

            if not self.is_collecting_data:
                car.hw1_target = car.id == hw1_car
                if not self.brake_wave:
                    car.hw2_target = car.id == hw2_car

            self.handle_braking(car)
            self.update_car(car)
            self.save_car_data(car)

            car = car.prev

        v = self.config.speed_limit
        dynamic_term = (v * (v - max(self.tail.speed, 10))) / (2 * self.config.braking_factor)
        s_star = self.config.car_length + self.config.target_distance + \
            max(0, v * self.config.time_headway + dynamic_term)
        if self.tail.position + self.config.car_length > s_star:
            self.create_car()
            # Offset because we don't have infinite updates / sec
            self.tail.position = s_star - self.tail.next.position - self.config.car_length

        self.valkey.set("head", self.head.id)
        self.valkey.set("tail", self.tail.id)

    def update_car(self, car: Car) -> None:
        if car.brake_amount:
            acceleration = car.brake_amount / 255 * 60 * self.config.update_interval
            car.speed = max(0, car.speed - acceleration)

        else:
            # Gradually restore reference speed up to original speed
            car.accel = idm(car, self.config)
            car.speed += car.accel * self.config.update_interval
            car.speed = max(0, car.speed)

        car.in_stopwave = False
        car.detected_stopwave = None
        for wave in self.stopwaves:  # Stopwaves are ordered where first is closest to end of the road
            if wave.in_range(car):
                car.detected_stopwave = wave  # Last one is the nearest
            if car in wave:
                car.in_stopwave = True

        car.position += car.speed * self.config.update_interval
        car.time_headway = self.get_recommended_headway(car)

        if (car.hw1_target or car.hw2_target):
            car.human_recommended_speed = self.get_human_recommended_speed(car)

    def get_human_recommended_speed(self, car: Car) -> int:
        if not car.detected_stopwave:
            return self.config.speed_limit

        cached_speed = car.speed
        for _ in range(5):
            accel = idm(car, self.config)
            car.speed += accel

        speed_to_send = car.speed
        car.speed = cached_speed

        return speed_to_send

    def get_recommended_headway(self, car: Car) -> int:
        if car.in_stopwave:
            return self.config.time_headway

        if not car.detected_stopwave:
            return self.config.time_headway

        return self.config.time_headway * self.config.headway_factor

    def get_recommended_speed(self, car: Car) -> int:
        if car.in_stopwave or not car.detected_stopwave or not car.is_smart or car.hw1_target:
            return car.recommended_speed + (self.config.speed_limit - car.recommended_speed) * self.config.recommend_interpolation_size

        distance_to_car_in_front = car.next.position - car.position
        recommended_speed = distance_to_car_in_front / (self.config.time_headway * self.config.headway_factor)

        speed_to_send = car.recommended_speed + \
            (recommended_speed - car.recommended_speed) * self.config.recommend_interpolation_size

        return speed_to_send

    def read_config(self) -> None:
        if get_val("reset", self.valkey, 0):
            self.clear()
            self.populate()
            self.valkey.set("reset", 0)

        start_brake_wave = get_val("brake_wave", self.valkey)
        if start_brake_wave and not self.brake_wave:
            self.start_brake_wave()

        start_data_collection = get_val("collect_data", self.valkey)
        if start_data_collection and not self.is_collecting_data:
            self.monte_carlo_step = self.config.monte_carlo_samples
            self.is_monte_carlo = self.config.monte_carlo_on != 0
            self.start_data_collection()

        self.config.read(self.valkey)

    def get_car_by_id(self, car_id: int) -> Car | None:
        car = self.head
        while car:
            if car.id == car_id:
                return car
            car = car.prev
        return None

    def detect_stopwaves(self) -> None:
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

    def serialize_cars(self) -> bytes:
        rep = bytes()
        car = self.head
        while car:
            rep += bytes(car)
            car = car.prev
        return rep

    def save_car_data(self, car: Car) -> None:
        if car.hw1_target:
            self.valkey.set("hw1_rec_speed", int(car.human_recommended_speed))
            self.valkey.set("hw1_speed", int(car.speed))
            self.valkey.set("hw1_urgency", car.brake_urgency)
        if car.hw2_target:
            self.valkey.set("hw2_rec_speed", int(car.human_recommended_speed))
            self.valkey.set("hw2_speed", int(car.speed))
            self.valkey.set("hw2_urgency", int(car.brake_urgency))

    def update_brake_wave(self) -> None:
        if self.brake_wave_samples == self.config.data_collection_brake_offset:
            car = self.get_car_by_id(self.config.data_collection_braking_car_id)
            car.brake_amount = self.config.data_collection_brake_pressure

        if self.brake_wave_samples >= self.config.data_collection_brake_samples\
                + self.config.data_collection_brake_offset:
            car = self.get_car_by_id(self.config.data_collection_braking_car_id)
            car.brake_amount = 0

            self.brake_wave_samples = 0
            self.brake_wave = False
        else:
            self.brake_wave_samples += 1

    def handle_braking(self, car: Car) -> None:
        if self.is_collecting_data:
            return

        if car.hw1_target:
            car.brake_amount = get_val("hw1_brake", self.valkey)

        if not car.hw1_target and not car.hw2_target:
            car.brake_amount = 0

        if self.brake_wave:
            return

        if car.hw2_target:
            car.brake_amount = get_val("hw2_brake", self.valkey)

    def create_car(self) -> Car:
        car = Car(config=self.config, id=self._id)
        self._id += 1
        if not self.head:
            self.head = car

        car.next = self.tail
        self.tail = car

        car.is_smart = random.random() < self.config.adoption_rate

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
        spawn_position = 65535  # Hardcode
        self.tail.position = spawn_position

        s_star = self.config.car_length + self.config.target_distance + \
            max(0, self.config.speed_limit * self.config.time_headway)
        spawn_position -= s_star

        while spawn_position >= 0:
            self.create_car()
            self.tail.position = spawn_position
            spawn_position -= s_star

    def start_brake_wave(self) -> None:
        self.valkey.set("brake_wave", 0)
        self.brake_wave = True
        car = self.get_car_by_id(self.config.data_collection_braking_car_id)
        car.hw2_target = True
        for _ in range(self.config.hw_1_offset):
            car = car.prev
        self.valkey.set("hw1_car", car.id)

    def start_data_collection(self) -> None:
        self.clear()
        self.populate()
        self.brake_wave = True
        target_cars = set(range(
            self.config.data_collection_braking_car_id,
            self.config.data_collection_braking_car_id +
            self.config.data_collection_count*self.config.data_collection_step,
            self.config.data_collection_step
        ))
        self.data = {
            i: {
                "id": i,
                "position": [],
                "speed": [],
                "accel": [],
                "gap": [],
            }
            for i in target_cars
        }

        car = self.head
        while car and target_cars:
            if car.id in target_cars:
                car.hw1_target = True
                target_cars.discard(car.id)
            car = car.prev

        self.is_collecting_data = True
        self.valkey.set("collect_data", 0)
        car = self.get_car_by_id(self.config.data_collection_braking_car_id)
        car.brake_amount = 0
        car.hw1_target = True
        car.hw2_target = True

    def stop_data_collection(self) -> None:
        self.is_collecting_data = False
        file_name = f"data_{datetime.now().strftime('%d-%m_%H:%M:%S')}.json"
        with open(file_name, "w") as f:
            json.dump(self.data, f)
        self.collected_samples = 0

        if self.is_monte_carlo and self.monte_carlo_step > 0:
            self.monte_carlo_step -= 1
            self.start_data_collection()

    def collect_data(self) -> None:
        print(f"Collecting data: {((self.collected_samples+1)/self.config.data_collection_samples)*100:2f}%")
        target_ids = set(range(
            self.config.data_collection_braking_car_id,
            self.config.data_collection_braking_car_id +
            self.config.data_collection_count*self.config.data_collection_step,
            self.config.data_collection_step
        ))
        car = self.head
        while car and target_ids:
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
