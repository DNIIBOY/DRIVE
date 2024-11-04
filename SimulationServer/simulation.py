from dataclasses import dataclass
import random
from valkey import Valkey
from car import Car
from driver import Driver
from time import sleep, time


@dataclass
class SimulationConfig:
    speed_limit: int = 200
    spawn_distance: int = 200
    kill_distance: int = 65535

    target_distance: int = 200
    speed_limit_deviation: int = 10

    update_interval: float = 0.05


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
        accel = 1.0
        if car._speed < self.config.speed_limit + car.driver.speed_limit_diff:
            accel = 1.1
        else:
            accel = 0.9

        if not car.next:
            car._speed *= accel
            car.position += int(car._speed * self.config.update_interval)
            return

        dist = car.next.position - car.position
        if dist > car.driver.target_distance:
            pass

        elif dist < car.driver.target_distance:
            accel = 0.9

        if dist == 0:
            pass

        car._speed *= accel
        car.position += int(car._speed * self.config.update_interval)

    def serialize_cars(self) -> bytes:
        rep = bytes()
        car = self.head
        while car:
            rep += bytes(car)
            car = car.prev
        return rep

    def create_car(self) -> Car:
        deviation = self.config.speed_limit_deviation
        driver = Driver(speed_limit_diff=random.randint(-deviation, deviation))
        car = Car(driver=driver, id=self._id)
        self._id += 1
        car._speed = 10
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
