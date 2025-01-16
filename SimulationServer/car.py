from __future__ import annotations
from config import SimulationConfig
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stopwave import StopWave


class Car:
    def __init__(
        self,
        config: SimulationConfig,
        id: int | None = None,
    ) -> None:
        self.id: int = id % 1024 if id is not None else 0

        self.in_stopwave = False
        self.detected_stopwave: StopWave = None

        self.hw1_target = False
        self.hw2_target = False

        self._next: Car = None
        self._prev: Car = None

        self.config = config

        self.is_smart = False

        self.accel = 0
        self.brake_amount = 0
        self.position = 0
        self.speed = config.speed_limit
        self.recommended_speed = self.config.speed_limit
        self.human_recommended_speed = self.config.speed_limit
        self.time_headway = self.config.time_headway

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

    @property
    def brake_urgency(self) -> int:
        """
        How far from the recommended speed the car is
        :return: Int from 0-5, where 0 is no urgency and 5 is the most urgent
        """
        if self.speed < self.recommended_speed:
            return 0
        diff = self.speed - self.recommended_speed
        return min(5, int(diff+36) // 36)

    def __repr__(self) -> str:
        return f"Car({self.id}), position: {self.position}, speed: {self.speed}, accel: {self.accel}, brake: {self.brake_amount}"

    def __hash__(self) -> int:
        return hash(self.id)

    def __bytes__(self) -> bytes:
        rep_int = int(max(0, self.position))
        rep_int &= (0xFFFF)  # Clear the upper 16 bits
        rep_int |= (self.id << 22)  # Set the id in the upper 10 bits
        rep_int |= (self.hw1_target << 16)  # Set the hw1_target in the 17th bit
        rep_int |= (self.hw2_target << 17)  # Set the hw2_target in the 18th bit

        # color = int(self.accel + 8)
        # color = min(15, max(0, accel))

        color = 8
        if self.detected_stopwave:
            color = 15

        if self.in_stopwave:
            color = 0

        rep_int |= color << 18  # Set the color in the 19th to 22th bit
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
