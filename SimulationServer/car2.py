from pid_control import PidControl
from random import randint as ri
from random import uniform as ui

SAFE_DISTANCE = 50  # Minimum distance between cars

class Car:
    def __init__(self, speed, start_x=0):
        """
        Initialize a car with a starting position and speed.
        Parameters:
        - speed: Speed of the car.
        - start_x: The initial x-coordinate of the car.
        """
        self.x = start_x  # Horizontal position on the road
        self.y = 0  # Vertical position will be set by main code if needed
        self.speed = speed
        self.original_speed = speed + ui(-0.1,1.5)  # Initial speed reference
        self.accel = 1.0
        self.width = 30
        self.height = 20
        self.color_r, self.color_g, self.color_b = ri(0, 255), ri(0, 255), ri(0, 255)

    def move(self):
        """Move the car by its current speed."""
        self.x += self.speed

    def get_position(self):
        """Get the car's current x position."""
        return self.x

    def check_collision_and_adjust_speed(self, car_in_front):
        """
        Adjust the car's speed based on proximity to the car in front
        and target speed.
        Parameters:
        - car_in_front: The car directly ahead of this car.
        """
        
        # Speed control to approach optimal speed
        p_speed = 0.35
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
        self.accel = max(0.3, min(self.accel, 1.1))  # Clamp accel to avoid extreme values

        # Update speed based on acceleration, ensuring it doesn’t exceed original speed
        self.speed *= self.accel
        self.speed = min(self.speed, self.original_speed)
        
        self.speed = max(0.1, self.speed)


        # Move car by its updated speed
        self.move()
