import math

from car import Car
from config import SimulationConfig
from random import uniform


def idm(car: Car, config: SimulationConfig):
    acceleration = 1

    if car.next:
        v = car.speed
        v0 = car.target_speed
        s0 = config.target_distance + uniform(10, 10)
        s = car.next.position - car.position + uniform(-10, 10)
        T = 2 + uniform(-1, 1)
        a_max = 1.5
        b = 2 + uniform(-1, 1)
        s_stjerne = s0 + (v * T) + (abs(car.next.speed - v) /
                                    2 * math.sqrt(a_max * b))

        acceleration = a_max * (1 - (v / v0) ** 4 - (s_stjerne / s) ** 2)

    return acceleration

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)
