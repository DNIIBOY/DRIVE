from random import randint as ri
from random import uniform as ui

from pid_control import PidControl
from settings import Settings

SAFE_DISTANCE = 50  # Minimum distance between cars


class Car:
    def __init__(self, start_x=0, special=False):
        """
        Initialize a car with a starting position and speed.
        Parameters:
        - speed: Speed of the car.
        - start_x: The initial x-coordinate of the car.
        """
        self.settings = Settings()
        self.x = start_x  # Horizontal position on the road
        self.y = 0  # Vertical position will be set by main code if needed
        self.speed = self.settings.car_speed
        self.speed_variation = self.settings.car_speed_variation
        self.original_speed = self.speed + ui(-self.speed_variation, self.speed_variation)  # Initial speed reference
        self.special = special
        self.accel = self.settings.car_accel
        self.width = self.settings.car_width
        self.height = self.settings.car_height
        self.color_r, self.color_g, self.color_b = 0, 255, 0

    def color_gradient(self, speed):
        # Ensure speed is within the range 0 to 2
        speed = max(0, min(2, speed))

        if speed <= 1:
            # Interpolate from red to green
            red = int(255 * (1 - speed))
            green = int(255 * speed)
            blue = 0
        else:
            # Interpolate from green to blue
            speed = speed - 1
            red = 0
            green = int(255 * (1 - speed))
            blue = int(255 * speed)
        self.color_r, self.color_g, self.color_b = red, green, blue

    def move(self):
        """Move the car by its current speed."""
        self.x += self.speed

    def get_position(self):
        """Get the car's current x position."""
        return self.x

    def get_speed(self):
        return self.speed

    def check_collision_and_adjust_speed(self, car_in_front):
        """
        Adjust the car's speed based on proximity to the car in front
        and target speed.
        Parameters:
        - car_in_front: The car directly ahead of this car.
        """
        if self.special and car_in_front:
            # Mere logic skal ind!!!############################################################
            self.speed = car_in_front.get_speed()

        # Speed control to approach optimal speed
        p_speed = 0.20
        speed_error = self.original_speed - self.speed
        control_speed = speed_error * p_speed

        # Distance control to avoid collision
        control_distance = 0
        if car_in_front:
            distance_to_front_car = car_in_front.get_position() - self.x
            if distance_to_front_car < SAFE_DISTANCE:
                p_dist = 2.2
                dist_error = SAFE_DISTANCE - distance_to_front_car
                control_distance = -dist_error * p_dist * 0.049

        # Combine speed and distance controls into acceleration factor
        self.accel = 1.0 + control_speed + control_distance
        self.accel = max(
            0.3, min(self.accel, 1.1)
        )  # Clamp accel to avoid extreme values

        # Update speed based on acceleration, ensuring it doesn’t exceed original speed
        self.speed *= self.accel
        self.speed = min(self.speed, self.original_speed)

        self.speed = max(0.1, self.speed)
        self.color_gradient(self.speed)
        # Move car by its updated speed
        self.move()
