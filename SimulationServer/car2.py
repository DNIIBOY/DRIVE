from pid_control import PidControl
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
        self.accel = 1.1

    def move(self, speed):
        """Move the car by its speed."""

        self.x += speed

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
            if car_in_front.get_position() == None:
                print("actual distance invalid")
                return
            if self.get_position() == None:
                print("self position invalid")
                return

            #print(car_in_front.get_position(), self.get_position())
            p_value = 2
            pid_error =  SAFE_DISTANCE - (car_in_front.get_position() - self.get_position())
            controloutput = pid_error * p_value  
            self.accel = 1.0 - 0.0045 * controloutput
            print(pid_error)

            #self.accel = PidControl.pid_calculator(SAFE_DISTANCE, car_in_front.get_position() - self.get_position())

        else:
            self.accel = 1.1


        self.move(self.speed * self.accel)