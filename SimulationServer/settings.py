from dataclasses import dataclass
from random import randint as ri

@dataclass
class Settings:
    car_accel: float = 1.0
    car_width: int = 30
    car_height: int = 20
    car_color_r: int = ri(0, 255)
    car_color_g: int = ri(0, 255)
    car_color_b: int = ri(0, 255)

 