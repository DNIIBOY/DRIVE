from dataclasses import dataclass


@dataclass
class SimulationConfig:
    initial_speed: int = 333
    speed_limit: int = 333
    spawn_distance: int = 500
    visual_speed_factor: int = 4
    kill_distance: int = 65565 * visual_speed_factor

    target_distance: int = 200
    speed_limit_deviation: int = 10

    update_interval: float = 0.05
    car_length: int = 100
    car_max_accel: float = 0.1
