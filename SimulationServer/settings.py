from dataclasses import dataclass
from random import randint as ri

@dataclass
class Settings:
    car_accel: float = 1.0
    car_width: int = 30
    car_height: int = 20


def pick_color():
    return ri(0, 255), ri(0, 255), ri(0, 255)

 
