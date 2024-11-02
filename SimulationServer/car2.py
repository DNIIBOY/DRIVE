# car2.py

SAFE_DISTANCE = 100  # Minimum distance between cars

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
        self.original_speed = speed  # Keep a reference to the car's initial speed
        self.width = 60  # Width of the car
        self.height = 40  # Height of the car

    def move(self):
        """Move the car by its speed."""
        self.x += self.speed

    def get_position(self):
        """Get the car's current x position."""
        return self.x

    def check_collision_and_slow_down(self, car_in_front):
        """
        Slow down the car if it's too close to the car in front.
        Parameters:
        - car_in_front: The car directly ahead of this car.
        """
        if car_in_front and (car_in_front.get_position() - self.x < SAFE_DISTANCE):
            self.speed = min(self.speed, car_in_front.speed - 1)
        else:
            self.speed = self.original_speed  # Reset speed if there's no car in front
