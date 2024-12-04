from __future__ import annotations
from car import Car


class StopWave:
    def __init__(self, start: Car, stop: Car) -> None:
        self.start = start
        self.stop = stop

        self._cars = set()
        car = self.start
        while car != self.stop:
            self._cars.add(car)
            car = car.prev
        self._cars.add(self.stop)

    def __repr__(self) -> str:
        return f"StopWave({self.start.id}, {self.stop.id})"

    def __contains__(self, car: Car) -> bool:
        return car in self._cars

    @classmethod
    def from_start(cls, start: Car, stop_wave_speed: float) -> StopWave:
        assert start.speed <= stop_wave_speed, "Car must be slower than stop wave speed"

        car = start
        while car.prev:
            if car.prev.speed > stop_wave_speed or not car.prev.is_smart:
                return cls(start, car)
            car = car.prev

        return cls(start, car)  # Car will always be the last car

    def in_range(self, car: Car) -> bool:
        """
        Detects stopwave
        """
        if car.position > self.start.position:
            return False

        return car.position + 10000 > self.stop.position

    @property
    def length(self) -> float:
        return self.start.position - self.stop.position
