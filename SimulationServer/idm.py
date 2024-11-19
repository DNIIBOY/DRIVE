import math

import numpy as np
from car import Car
from config import SimulationConfig


def idm(car: Car, config: SimulationConfig):
    v = car.speed  # Aktuelle hastighed
    v0 = 277  # car.reference_speed  # Ønskede hastighed
    a_max = config.car_max_accel  # Max acceleration

    if car.next:
        delta_v = car.next.speed - car.speed
        s0 = config.target_distance  # Ønskede minimum afstand
        s = max(car.next.position - car.position - config.car_length, 0.01)

        T = 0.5  # "Time Headway", den ønskede afstand til forankørende bil i sekunder
        b = 20  # Komfortabel bremseværdi

        distance_perception_deviation = np.random.normal(
            0, 1
        )  # En normalfordeling til percieved distance
        s_percieved = max(s + distance_perception_deviation, 0.01)

        accel_formular_term_1 = (v / v0) ** 4
        s_star = (s0 + T * v
            + max((v * delta_v) / (2 * math.sqrt(max(a_max, 1) * max(b, 1))), 0)
        )

        accel_formular_term_2 = (
            s_star / s_percieved
        ) ** 4  # Reducer exponent for at få mindre aggressiv bremse
        acceleration = a_max * \
            (1 - accel_formular_term_1 - accel_formular_term_2)
    else:
        acceleration = a_max * (1 - (v / v0) ** 2)  # Hvad er det her?

    return acceleration

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)
