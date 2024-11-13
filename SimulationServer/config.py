from dataclasses import dataclass
from valkey import Valkey


@dataclass
class SimulationConfig:
    
    initial_speed: int = 50
    speed_limit: int = 100
    kill_distance: int = 65535

    spawn_distance: int = 70
    target_distance: int = 70
    speed_limit_deviation: int = 0

    update_interval: float = 0.05
    car_length: int = 15
    car_max_accel: float = 1.3

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
