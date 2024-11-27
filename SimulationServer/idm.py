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

        if car.estimated_gap is None:
            car.estimated_gap = s
        if car.delta_v_percieved is None:
            car.delta_v_percieved = delta_v

        # Calculate new random values with adjusted spread
        spread_factor = max(0.05, min(0.5, s / 80.0))  # Adjust spread factor based on s
        new_estimated_gap = max(np.random.normal(s, config.percieved_distance_spread * s * spread_factor), 0.01)
        new_delta_v_percieved = np.random.normal(delta_v, config.percieved_speed_spread)

        # update the values
        alpha = 0.1
        car.estimated_gap = max((1 - alpha) * car.estimated_gap + alpha * new_estimated_gap, 0.5)  # Ensure a minimum gap
        car.delta_v_percieved = (1 - alpha) * car.delta_v_percieved + alpha * new_delta_v_percieved

        accel_formular_term_1 = (v / v0) ** 4

        dynamic_term = (v * car.delta_v_percieved) / (2 * config.braking_factor)
        s_star = s0 + T * v + max(0, dynamic_term)
        # Reducer exponent for at få mindre aggressiv bremse
        accel_formular_term_2 = (s_star / car.estimated_gap) ** 2
        acceleration = a_max * (1 - accel_formular_term_1 - accel_formular_term_2)
    else:
        acceleration = a_max * (1 - (v / v0) ** 2)

    return acceleration

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)
