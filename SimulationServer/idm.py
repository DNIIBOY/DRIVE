import math

import numpy as np
from car import Car
from config import SimulationConfig


def idm(car: Car, config: SimulationConfig):
    v = car.speed  # Aktuelle hastighed
    # car.reference_speed  # Ønskede hastighed
    v0 = np.random.normal(config.speed_limit, config.speed_limit_deviation)
    a_max = config.car_max_accel  # Max acceleration

    if car.next:
        delta_v = car.next.speed - car.speed
        s0 = config.target_distance  # Ønskede minimum afstand
        s = max(car.next.position - car.position - config.car_length, 0.01)

        # "Time Headway", den ønskede afstand til forankørende bil i sekunder
        T = config.time_headway

        # Stokastisk relativ hastighed

        # Normalfordelt afstandsbedømmelse
        estimated_gap = max(np.random.normal(s, config.percieved_distance_spread), 0.01)  # Normal value 0.1
        delta_v_percieved = np.random.normal(delta_v, config.percieved_speed_spread)  # Normal value 0.1
        # if s > config.percieved_cut_off:
        # else:
        #     estimated_gap = s
        #     delta_v_percieved = delta_v
        accel_formular_term_1 = (v / v0) ** 4

        dynamic_term = (v * delta_v_percieved) / (2 * config.braking_factor)
        s_star = s0 + T * v + (dynamic_term if dynamic_term > 0 else 0)
# Reducer exponent for at få mindre aggressiv bremse
        accel_formular_term_2 = (s_star / estimated_gap) ** 2
        acceleration = a_max * (1 - accel_formular_term_1 - accel_formular_term_2)
    else:
        acceleration = a_max * (1 - (v / v0) ** 2)

    return acceleration

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)
