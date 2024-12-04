from dataclasses import dataclass
from valkey import Valkey
from functools import lru_cache
from operator import attrgetter


def cached_property_depends_on(*args):
    attrs = attrgetter(*args)

    def decorator(func):
        _cache = lru_cache(maxsize=None)(lambda self, _: func(self))

        def _with_tracked(self):
            return _cache(self, attrs(self))
        return property(_with_tracked, doc=func.__doc__)
    return decorator


@dataclass
class SimulationConfig:
    speed_limit: int = 277
    stop_wave_factor: float = 0.3

    kill_distance: int = 65535
    car_length: int = 25

    target_distance: int = 50
    update_interval: float = 0.05
    car_max_accel: float = 10

    time_headway: float = 1
    comfortable_breaking_value: float = 15

    adoption_rate: float = 0.1
    headway_factor: float = 1.0

    drive_activated: int = 1
    real_time: int = 1

    data_collection_brake_offset: int = 250
    data_collection_brake_pressure: int = 150
    data_collection_brake_samples: int = 100
    data_collection_brake_samples: int = 120
    data_collection_braking_car_id: int = 130
    data_collection_count: int = 10
    data_collection_samples: int = 3500
    data_collection_step: int = 5

    @property
    def stop_wave_speed(self) -> float:
        return self.speed_limit * self.stop_wave_factor

    @cached_property_depends_on("car_max_accel", "comfortable_breaking_value")
    def braking_factor(self) -> float:
        return (self.car_max_accel * self.comfortable_breaking_value) ** 0.5

    def read(self, valkey: Valkey) -> None:
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            val = valkey.get(key)

            if val is not None:
                setattr(self, key, type(value)(val.decode()))

    def save(self, valkey: Valkey) -> None:
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            valkey.set(key, value)

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_")}

    def __hash__(self) -> int:
        return hash(frozenset(self.to_dict().items()))
