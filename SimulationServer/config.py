from dataclasses import dataclass
from valkey import Valkey


@dataclass
class SimulationConfig:
    visual_speed_factor: int = 10
    initial_speed: int = 300
    speed_limit: int = 333
    spawn_distance: int = 250 #* visual_speed_factor
    kill_distance: int = 65565 * visual_speed_factor

    target_distance: int = 100 #* visual_speed_factor
    speed_limit_deviation: int = 0

    update_interval: float = 0.05
    car_length: int = 300
    car_max_accel: float = 0.01
