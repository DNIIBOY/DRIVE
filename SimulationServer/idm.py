import math
from car import Car
from config import SimulationConfig

def idm(car: Car, config: SimulationConfig):
    acceleration = 1

    if car.next:
        v = car.speed
        v0 = car.target_speed
        s0 = config.target_distance
        s = car.next.position - car.position
        T = 2
        a_max = 1.5
        b = 2
        s_stjerne = s0 + (v * T) + (abs(car.next.speed-v) / 2 * math.sqrt(a_max*b))

        acceleration = a_max*(1-(v/v0)**4 - (s_stjerne/s)**2)
        
    return acceleration

        # Vores system skal KLARE de stokatiske udfordringer
        # Fastlæg behov.
        # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)


