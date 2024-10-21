class Driver:
    """
    Driver class to store driver's parameters.
    :param reaction_time: Reaction time of the driver in seconds.
    :param speed_limit_ratio: The max ratio of the speed limit that the driver will drive at.
    """

    def __init__(
        self,
        reaction_time: float = 0.3,
        speed_limit_ratio: float = 1.0,
    ) -> None:
        self.reaction_time = reaction_time
        self.speed_limit_ratio = speed_limit_ratio
