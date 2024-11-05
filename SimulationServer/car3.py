from random import uniform as ui

from settings import Settings

SAFE_DISTANCE = 50  # Minimum distance between cars


def pid_calculator(car, target_distance, car_position, car_in_front):
    acceleration = 0
    # Speed control to approach reference speed
    p_speed = 0.20
    speed_error = car.reference_speed - car._speed
    control_speed = speed_error * p_speed

    # Distance control to avoid collision
    control_distance = 0
    if car_in_front:
        distance_to_front_car = car_in_front._position - car_position
        if distance_to_front_car < target_distance:
            p_dist = 2.2
            dist_error = target_distance - distance_to_front_car
            control_distance = -dist_error * p_dist * 0.049

    acceleration = 1.0 + control_speed + control_distance
    acceleration = max(0.3, min(acceleration, 1.1))
    return acceleration


class Car:
    def __init__(self):
        """
        Initialize a car with a starting position and speed.
        Parameters:
        - speed: Speed of the car.
        - start_x: The initial x-coordinate of the car.
        """
        self.settings = Settings()
        self.position = 0
        self.speed = self.settings.car_speed
        self.speed_variation = self.settings.car_speed_variation
        self.original_speed = self.speed + \
            ui(-self.speed_variation, self.speed_variation)  # Initial speed reference
        self.reference_speed = self.original_speed  # Target speed for P-controller to achieve
        self.accel = self.settings.car_accel
        self.length = self.settings.car_length
        self.brake_amount = 0  # Amount of speed reduction when braking
        self.max_speed_increase_per_second = self.settings.max_speed_increase_per_second

    def check_collision_and_adjust_speed(self, car_in_front):
        """
        Adjust the car's speed based on proximity to the car in front
        and target speed.
        Parameters:
        - car_in_front: The car directly ahead of this car.
        """
        # Update reference speed based on braking status
        if self.brake_amount:
            # Decrease reference speed by brake_amount, but not below 0
            self.reference_speed = max(0, self.reference_speed - self.brake_amount)
        else:
            # Gradually restore reference speed up to original speed
            if self.reference_speed < self.original_speed:
                self.reference_speed = min(
                    self.original_speed,
                    self.reference_speed + self.max_speed_increase_per_second
                )

        self.accel = pid_calculator(self, SAFE_DISTANCE, self.position, car_in_front)

        self.speed *= self.accel
        self.speed = min(self.speed, self.original_speed)
        self.speed = max(0.1, self.speed)
        self.position += self.speed
