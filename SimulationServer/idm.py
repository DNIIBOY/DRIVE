import math

import numpy as np
from car import Car
from config import SimulationConfig


def idm(car: Car, config: SimulationConfig):
    v = car.speed  # Aktuelle hastighed
    # car.reference_speed  # Ønskede hastighed
    #v0 = np.random.normal(config.speed_limit, config.speed_limit_deviation)
    v0 = car.recommended_speed
    a_max = config.car_max_accel  # Max acceleration

    if car.next:
        delta_v = car.speed - car.next.speed
        s0 = config.target_distance + config.car_length  # Ønskede minimum afstand
        s = max(car.next.position - car.position - config.car_length, 0.01)

        # "Time Headway", den ønskede afstand til forankørende bil i sekunder
        T = car.time_headway

        accel_formular_term_1 = (v / v0) ** 4

        dynamic_term = (v * delta_v) / (2 * config.braking_factor)
        s_star = s0 + max(0, T * v + dynamic_term)
        # Reducer exponent for at få mindre aggressiv bremse
        accel_formular_term_2 = (s_star / s) ** 2
        acceleration = a_max * (1 - accel_formular_term_1 - accel_formular_term_2)
    else:
        if car.speed < config.speed_limit:
            acceleration = a_max * (1 - (v / v0) ** 4)
        else:
            acceleration = 0

    return acceleration

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)


def adapt_stopwave(car: Car, config: SimulationConfig, should_be_active: bool):

    pass