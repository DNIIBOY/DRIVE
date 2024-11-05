import random
from valkey import Valkey
from car import Car
from time import sleep, time
from config import SimulationConfig
from pid_control import pid_calculator


class Simulation:
    def __init__(self, valkey: Valkey) -> None:
        self.valkey = valkey
        self.head: Car = None
        self.tail: Car = None
        self.config = self._read_config()
        self._id = 0
        self.create_car()

    def _read_config(self) -> SimulationConfig:
        config = SimulationConfig()
        for key, val in config.__dict__.items():
            val = self.valkey.get(key)
            if val is not None:
                setattr(config, key, val)
        return config

    def main_loop(self) -> None:
        while True:
            start_time = time()
            self.update_cars()
            self.valkey.set("cars", self.serialize_cars())
            elapsed_time = time() - start_time
            sleep(self.config.update_interval - elapsed_time)

    def update_cars(self) -> None:
        car = self.head
        while car:
            if car.position > self.config.kill_distance:
                self.destroy_car(car)
                car = car.prev
                continue

            self.update_car(car)
            car = car.prev

        if self.tail.position > self.config.spawn_distance:
            self.create_car()

    def update_car(self, car: Car) -> None:
        if car.brake_amount:
            # Decrease reference speed by brake_amount, but not below 0
            car.reference_speed = max(0, car.reference_speed - car.brake_amount)
        else:
            # Gradually restore reference speed up to original speed
            if car.reference_speed < car.target_speed:
                car.reference_speed = min(
                    car.original_speed,
                    car.reference_speed + car.max_ref_inc
                )

        car.accel = pid_calculator(car, self.config)
        car.speed *= car.accel
        car.speed = min(car.speed, car.target_speed)
        car.speed = max(0.1, car.speed)
        car.position += car.speed

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
