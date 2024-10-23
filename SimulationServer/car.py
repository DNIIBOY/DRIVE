from __future__ import annotations
from driver import Driver


class Car:
    def __init__(
        self,
        driver: Driver = None,
    ) -> None:
        self._speed = 0
        self._position = 0
        self._is_target = False
        self.driver = driver

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
        rep_int = self._position
        if self._is_target:
            rep_int |= 1 << 15
        else:
            rep_int &= ~(1 << 15)
        return rep_int.to_bytes(2, byteorder="big")


def main():
    cars = [Car() for _ in range(10)]
    rep = bytes()
    for car in cars:
        rep += bytes(car)
    print(rep)
    print(len(rep))


if __name__ == "__main__":
    main()
