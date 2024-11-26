from __future__ import annotations
from config import SimulationConfig
import random
from time import time

class Car:
    def __init__(
        self,
        config: SimulationConfig,
        id: int | None = None,
    ) -> None:
        self.id: int = id % 1024 if id is not None else 0
        self.is_stopwaving = False
        self.seeing_traffic = False

        self.hw1_target = False
        self.hw2_target = False

        self._next: Car = None
        self._prev: Car = None

        self.config = config

        self.accel = 0
        self.brake_amount = 0
        self._position = 0
        self.speed = self.config.initial_speed

        self.speed_limit_diff = random.uniform(-self.config.speed_limit_deviation,
                                               self.config.speed_limit_deviation)
        self.reference_speed = self.target_speed + self.speed_limit_diff

        self.max_ref_inc = self.config.car_max_accel
        self.time_to_next_reaction = time()

    @property
    def position(self) -> float:
        return self._position

    @position.setter
    def position(self, value: float) -> None:
        self._position = min(value, self.config.kill_distance)

    @property
    def target_speed(self) -> int:
        return self.config.speed_limit + self.speed_limit_diff

    @property
    def next(self) -> Car:
        return self._next

    @next.setter
    def next(self, next_car: Car) -> None:
        self._next = next_car
        if next_car:
            next_car._prev = self

    @property
    def prev(self) -> Car:
        return self._prev

    @prev.setter
    def prev(self, prev_car: Car) -> None:
        self._prev = prev_car
        if prev_car:
            prev_car._next = self

    def __hash__(self) -> int:
        return hash(self.id)

    def __bytes__(self) -> bytes:
        rep_int = int(self.position)
        rep_int &= (0xFFFF)  # Clear the upper 16 bits
        rep_int |= (self.id << 22)  # Set the id in the upper 10 bits
        rep_int |= (self.hw1_target << 16)  # Set the hw1_target in the 17th bit
        rep_int |= (self.hw2_target << 17)  # Set the hw2_target in the 18th bit

        # accel = int(self.accel + 8)
        # accel = min(15, max(0, accel))

        accel = 8

        if self.seeing_traffic:
            accel = 15

        if self.is_stopwaving:
            accel = 0

        rep_int |= accel << 18  # Set the acceleration in the 19th to 22th bit
        return rep_int.to_bytes(4, byteorder="big")


def main():
    def bytes_to_bits(byte_data):
        # Convert each byte in the bytes object to its binary representation
        return "".join(f"{byte:08b}" for byte in byte_data)

    cars = [Car(i, SimulationConfig()) for i in range(1)]
    cars[0].position = 65535
    cars[0].id = 1023
    cars[0].hw2_target = True
    rep = bytes()
    for car in cars:
        rep += bytes(car)
    print(bytes_to_bits(rep))
    print(rep)


if __name__ == "__main__":
    main()
