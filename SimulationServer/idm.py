import math

from car import Car
from config import SimulationConfig


def idm(car: Car, config: SimulationConfig):
    v = car.speed  # Aktuelle hastighed
    v0 = 277  # car.reference_speed  # Ønskede hastighed
    a_max = config.car_max_accel  # Max acceleration

    if car.next:
        delta_v = car.next.speed - car.speed
        s0 = config.target_distance  # Ønskede minimum afstand
        s = max(car.next.position - car.position, 0.01)  # + config.car_length  # Aktuelle afstand
        T = 0.5  # "Time Headway", den ønskede afstand til forankørende bil i sekunder
        b = 20  # Komfortabel bremseværdi
        
        distance_perception_deviation = np.random.normal(0, 10) # En normalfordeling til percieved distance
        s_percieved = s + distance_perception_deviation

        accel_formular_term_1 = (v / v0)**4
        s_star = s0 + T * v + (v * delta_v) / (2 * math.sqrt(a_max * b))
        accel_formular_term_2 = s_star / s_percieved
        acceleration = a_max * (1 - accel_formular_term_1 - accel_formular_term_2**2)
    else:
        acceleration = a_max * (1 - (v / v0)**2) # Hvad er det her?

    return acceleration * config.update_interval


    #  # Når target_distance bliver højere varierer accel mere. I starten lige nu bremser alle biler, hvilket ikke giver mening. 
    # Vi skal have kigget på spawn og på hvilke variabler der ikke bliver brugt som feks speed_limit og speed_limit_deviation 


    # Vores system skal KLARE de stokatiske udfordringer
    # Fastlæg behov.
    # Gå tilbage, interessantanalyse, problemanalyse (Til seminar)
