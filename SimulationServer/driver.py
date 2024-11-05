from random import uniform


class Driver:
    """
    Driver class to store driver's parameters.
    :param reaction_time: Reaction time of the driver in seconds.
    :param target_distance: The distance the driver will keep from the car in front.
    """

    def __init__(
        self,
        # Et menneskes reaktionshastighed er på mellem 100-300 millisekund
        reaction_time: float = round(uniform(0.1, 0.3), 5),
        target_distance: int = 200,
        speed_limit_diff: int = 0,
    ) -> None:
        self.reaction_time = reaction_time
        self.target_distance = target_distance
        self.speed_limit_diff = speed_limit_diff


def main():
    dr = Driver()
    print(dr.reaction_time)


if __name__ == "__main__":
    main()
