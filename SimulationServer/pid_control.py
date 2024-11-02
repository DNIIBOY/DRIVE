class PidControl: 
    def __init__(self) -> None:
        self.p_value = 1


    def pid_calculator(self, target_distance, actual_distance):

        pid_error =  target_distance - actual_distance
        controloutput = pid_error * self.p_value  

        return 1.0 - 0.0045 * controloutput