import math

from car import Car
from config import SimulationConfig
from random import uniform


def idm(car: Car, config: SimulationConfig):
    acceleration = 1

    if car.next:
        v = car.speed
        v0 = car.target_speed + uniform(-30, 30) 
        s0 = config.target_distance 
        s = car.next.position - car.position + uniform(-10, 10)
        T = 1.5
        a_max = 1.3
        b = 0.3
        s_stjerne = s0 + (v * T) + (abs(car.next.speed - v) /
                                    2 * math.sqrt(a_max * b))

        acceleration = a_max * ((1 - ((v / v0) ** 4) - (s_stjerne / s) ** 2))

    return acceleration

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)
