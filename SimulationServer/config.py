from dataclasses import dataclass
from valkey import Valkey


@dataclass
class SimulationConfig:
    initial_speed: int = 333
    speed_limit: int = 333
    spawn_distance: int = 10
    visual_speed_factor: int = 4
    base_kill_distance: int = 65565

    target_distance: int = 200
    speed_limit_deviation: int = 10

    update_interval: float = 0.05
    car_length: int = 300
    car_max_accel: float = 0.1

    def read(self, valkey: Valkey) -> None:
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            val = valkey.get(key)

            if val is not None:
                setattr(self, key, value)

    def save(self, valkey: Valkey) -> None:
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            valkey.set(key, value)

    @property
    def kill_distance(self) -> int:
        return self.base_kill_distance * self.visual_speed_factor

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_")}
