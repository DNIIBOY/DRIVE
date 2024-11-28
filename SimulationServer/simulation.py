from car import Car
from config import SimulationConfig
from idm import idm
from stopwave import StopWave
from time import sleep, time
from valkey import Valkey


class Simulation:
    def __init__(self, valkey: Valkey) -> None:
        self._id = 0
        self.valkey = valkey
        self.head: Car = None
        self.tail: Car = None

        self.config = SimulationConfig()
        self.config.read(valkey)

        self.stopwaves: list[StopWave] = []

        self.create_car()

    def main_loop(self) -> None:
        config_refresh_time = time()
        while True:
            if time() - config_refresh_time > 1:
                self.config.read(self.valkey)
                config_refresh_time = time()
            start_time = time()
            self.update_cars()
            self.valkey.set("cars", self.serialize_cars())
            elapsed_time = time() - start_time
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
            if car.next.speed > self.config.stop_wave_speed:
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

        v_chase = self.tail.speed
        v = self.config.speed_limit
        dynamic_term = (v * (v - max(self.tail.speed, 10))) / (2 * self.config.braking_factor)
        s_star = self.config.car_length + self.config.target_distance + max(0, v * self.config.time_headway + dynamic_term)
        if self.tail.position + self.config.car_length > s_star:
            #print(f"V is {v}, self.tail.speed is {self.tail.speed}, s_star is {s_star}. Dynamic tem is {dynamic_term}")
            self.create_car()
            # Offset because we don't have infinite updates / sec
            #self.tail.speed = v_chase
            self.tail.position = max(0, s_star - self.tail.next.position - self.config.car_length)

        self.valkey.set("head", self.head.id)
        self.valkey.set("tail", self.tail.id)

    def update_car(self, car: Car) -> None:
        if car.brake_amount:
            # Decrease reference speed by brake_amount, but not below 0
            # car.reference_speed = max(0.1, car.reference_speed - car.brake_amount)
            # car.accel = 1 - (car.brake_amount / 255)
            acceleration = car.brake_amount / 255 * 60 * 0.3
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
        car.recommended_speed = self.get_recommended_speed(car)

    def get_recommended_speed(self, car: Car) -> int:
        if car.in_stopwave:
            return 0

        if not car.detected_stopwave:
            return car.target_speed

        return car.detected_stopwave.stop.speed

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


def main():
    valkey = Valkey(host="localhost", port=6379, db=0)
    sim = Simulation(valkey)
    print(sim.config.__dict__)


if __name__ == "__main__":
    main()
