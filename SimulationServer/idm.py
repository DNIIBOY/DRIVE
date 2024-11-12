import math
from random import uniform

from car import Car
from config import SimulationConfig
from time import time


def idm(car: Car, config: SimulationConfig):
    acceleration = 1

    if car.next:
        if time() > car.time_to_next_reaction:
            v = car.speed
            v0 = car.reference_speed  # + uniform(-15, 15)
            s0 = config.target_distance  # + uniform(-30, 30)
            s = max(car.next.position - car.position, 0.01)
            T = 5
            a_max = 1.3 + uniform(-0.1, 0.1)
            b = 20
            s_stjerne = s0 + (v * T) + (abs(car.next.speed - v) / 2 * math.sqrt(a_max * b))

            acceleration = a_max * ((1 - ((v / v0) ** 4) - (s_stjerne / s) ** 2))
            car.time_to_next_reaction = time()
            if abs(car.accel - acceleration) > 20:
                car.time_to_next_reaction += 0.2
        else:
            acceleration = car.accel

    return acceleration

    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)

    # Reaktionstid? counter % 3 == 0 eller time?
    # If elapsed time > 10:
    #    idm
    #    elapsed time = 0
    # else:
    #    pass
