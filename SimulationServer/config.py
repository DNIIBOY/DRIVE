from dataclasses import dataclass
from valkey import Valkey


@dataclass
class SimulationConfig:
    initial_speed: int = 277
    speed_limit: int = 277
    kill_distance: int = 65535
    car_length: int = 15

    spawn_distance: int = 700
    target_distance: int = 25
    update_interval: float = 0.05
    car_max_accel: float = 30

    time_headway: float = 1.5
    comfortable_breaking_value: float = 20

    speed_limit_deviation: int = 0
    percieved_distance_spread: float = 1
    percieved_speed_spread: float = 1
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
