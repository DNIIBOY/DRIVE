from dataclasses import dataclass
from valkey import Valkey


@dataclass
class SimulationConfig:
    visual_speed_factor: int = 10
    initial_speed: int = 300
    speed_limit: int = 333
<<<<<<< HEAD
    spawn_distance: int = 250 #* visual_speed_factor
    kill_distance: int = 65565 * visual_speed_factor
=======
    spawn_distance: int = 10
    visual_speed_factor: int = 4
    base_kill_distance: int = 65565
>>>>>>> de403bfb04ec7bc0ab1743b0d4ea76c1fb68b52d

    target_distance: int = 100 #* visual_speed_factor
    speed_limit_deviation: int = 0

    update_interval: float = 0.05
    car_length: int = 300
<<<<<<< HEAD
    car_max_accel: float = 0.01
=======
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
>>>>>>> de403bfb04ec7bc0ab1743b0d4ea76c1fb68b52d
