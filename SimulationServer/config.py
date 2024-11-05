from dataclasses import dataclass


@dataclass
class SimulationConfig:
    initial_speed: int = 15
    speed_limit: int = 200
    spawn_distance: int = 200
    kill_distance: int = 10000

    target_distance: int = 200
    speed_limit_deviation: int = 10

    update_interval: float = 0.05
    car_length: int = 30
    car_max_accel: float = 0.1
