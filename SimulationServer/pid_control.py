from car import Car
from config import SimulationConfig


def pid_calculator(car: Car, config: SimulationConfig) -> float:
    acceleration = 0
    # Speed control to approach reference speed
    p_speed = 0.20
    speed_error = car.reference_speed - car.speed
    control_speed = speed_error * p_speed

    # Distance control to avoid collision
    control_distance = 0
    if car.next:
        distance_to_front_car = car.next.position - car.position - config.car_length
        if distance_to_front_car < config.target_distance:
            p_dist = 2.2
            dist_error = config.target_distance - distance_to_front_car
            control_distance = -dist_error * p_dist * 0.049

    acceleration = 1.0 + control_speed + control_distance
    acceleration = max(0.3, min(acceleration, 1.1))
    return acceleration
