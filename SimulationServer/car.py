from __future__ import annotations
from driver import Driver


class Car:
    def __init__(
        self,
        id: int | None = None,
        driver: Driver = None,
    ) -> None:
        self.id: int = id % 1024 if id is not None else 0
        self.speed = 0
        self.position = 0
        self.driver = driver

        self.hw1_target = False
        self.hw2_target = False

        self._next: Car = None
        self._prev: Car = None

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

    def __bytes__(self) -> bytes:
        rep_int = self.position
        rep_int &= (0xFFFF)  # Clear the upper 16 bits
        rep_int |= (self.id << 22)  # Set the id in the upper 10 bits
        rep_int |= (self.hw1_target << 16)  # Set the hw1_target in the 17th bit
        rep_int |= (self.hw2_target << 17)  # Set the hw2_target in the 18th bit
        return rep_int.to_bytes(4, byteorder="big")


def main():
    def bytes_to_bits(byte_data):
        # Convert each byte in the bytes object to its binary representation
        return "".join(f"{byte:08b}" for byte in byte_data)

    cars = [Car() for _ in range(1)]
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
