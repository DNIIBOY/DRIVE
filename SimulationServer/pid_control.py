class PidControl:
    def __init__(self) -> None:
        self.p_value = 1

    def pid_calculator(self, target_distance, car_in_front, car_position):
        acceleration = 0
        # Speed control to approach reference speed
        p_speed = 0.20
        speed_error = self.reference_speed - self._speed
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
