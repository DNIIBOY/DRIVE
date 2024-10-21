from __future__ import annotations
from driver import Driver


class Car:
    def __init__(
        self,
        driver: Driver = None,
        next: Car = None,
        prev: Car = None,
    ) -> None:
        self._speed = 0
        self._position = 0
        self._is_target = False

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
