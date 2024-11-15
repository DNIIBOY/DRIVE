import math
from random import uniform

from car import Car
from config import SimulationConfig
from time import time


def idm(car: Car, config: SimulationConfig):
    acceleration = 0

    # if car.next:
    #     if time() > car.time_to_next_reaction:
    #         v = car.speed # Aktuelle hastighed
    #         v0 = car.reference_speed  # Ønskede hastighed
    #         s0 = config.target_distance  # Ønskede minimum afstand
    #         s = max(car.next.position - car.position, 0.01) # Aktuelle afstand
    #         T = 5 # "Time Headway", den ønskede afstand til forankørende bil i sekunder
    #         a_max = config.car_max_accel # Max acceleration
    #         b = 20 # Komfortabel bremseværdi
    #         s_stjerne = s0 + (v * T) + (abs(car.next.speed - v) / 2 * math.sqrt(a_max * b)) # Hastighedsbetinget afstand

    #         acceleration = a_max * ((1 - ((v / v0) ** 4) - (s_stjerne / s) ** 2)) * config.update_interval
    #         car.time_to_next_reaction = time()
    #         if abs(car.accel - acceleration) > 20:
    #             car.time_to_next_reaction += 0.2
    #     else:
    #         acceleration = car.accel

    if car.next:
        v = car.speed # Aktuelle hastighed
        v0 = 277 #car.reference_speed  # Ønskede hastighed
        delta_v = car.next.speed - car.speed
        s0 = config.target_distance  # Ønskede minimum afstand
        s = max(car.next.position - car.position, 0.01) # Aktuelle afstand
        T = 2 # "Time Headway", den ønskede afstand til forankørende bil i sekunder
        a_max = config.car_max_accel # Max acceleration
        b = 20 # Komfortabel bremseværdi

        accel_formular_term_1 = 1 - (v / v0)**4
        accel_formular_term_2 = (s0 + T * v - s + (v * delta_v) / (2 * math.sqrt(a_max * b)))
        acceleration = a_max * accel_formular_term_1 * accel_formular_term_2

        if car.id == 1:
            print(f"Rel dist: {car.next.position - car.position}, speed: {car.speed}, accel: {acceleration}")
    return acceleration * config.update_interval

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)

    # Reaktionstid? counter % 3 == 0 eller time?
    # If elapsed time > 10:
    #    idm
    #    elapsed time = 0
    # else:
    #    pass
