from car import Car
from config import SimulationConfig


def idm(car: Car, config: SimulationConfig):
    v = car.speed  # Current speed
    v0 = car.recommended_speed
    a_max = config.car_max_accel  # Max acceleration

    if car.next:
        delta_v = car.speed - car.next.speed
        s0 = config.target_distance + config.car_length  # Minimum distance to next car
        s = max(car.next.position - car.position - config.car_length, 0.01)

        # "Time Headway", the time it would take to reach the next car at the current speed
        T = car.time_headway

        accel_formular_term_1 = (v / v0) ** 4

        dynamic_term = (v * delta_v) / (2 * config.braking_factor)
        s_star = s0 + max(0, T * v + dynamic_term)
        accel_formular_term_2 = (s_star / s) ** 2
        acceleration = a_max * (1 - accel_formular_term_1 - accel_formular_term_2)
    else:
        if car.speed < config.speed_limit:
            acceleration = a_max * (1 - (v / v0) ** 4)
        else:
            acceleration = 0

    return acceleration
