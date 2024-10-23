class Driver:
    """
    Driver class to store driver's parameters.
    :param reaction_time: Reaction time of the driver in seconds.
    :param target_distance: The distance the driver will keep from the car in front.
    """

    def __init__(
        self,
        reaction_time: float = 0.3,
        target_distance: int = 200,
        speed_limit_diff: int = 0,
    ) -> None:
        self.reaction_time = reaction_time
        self.target_distance = target_distance
        self.speed_limit_diff = speed_limit_diff
