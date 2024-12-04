from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import json
from sys import argv

from itertools import cycle


def load_data(file_path: str = "data.json") -> pd.DataFrame:
    """
    Load the data from the JSON file.
    The inner lists will be numpy arrays
    :param file_path: Path to the file
    :return: DataFrame
    """
    cars = {}
    with open(file_path, "r") as file:
        data = json.load(file)

    for car, values in data.items():
        for key, value in values.items():
            values[key] = np.array(value)
        del values["id"]
        cars[car] = pd.DataFrame(values)
    return cars


class CarPlotter:
    def __init__(
        self,
        cars: dict[str, pd.DataFrame],
    ) -> None:
        self.cars = cars
        self.disabled_ids = set()
        self.take_mean = False

    def disable_car(self, car: str) -> None:
        assert car in self.cars, f"Car {car} not found"
        self.disabled_ids.add(car)

    def enable_car(self, car: str) -> None:
        assert car in self.cars, f"Car {car} not found"
        self.disabled_ids.remove(car)

    def disable_all(self) -> None:
        self.disabled_ids = set(self.cars.keys())

    def enable_all(self) -> None:
        self.disabled_ids = set()

    def mean(self) -> pd.DataFrame:
        return pd.concat(self.enabled_cars.values()).groupby(level=0).mean()

    @property
    def enabled_cars(self) -> dict[str, pd.DataFrame]:
        return {car: data for car, data in self.cars.items() if car not in self.disabled_ids}

    def plot(self, column: str = "position") -> None:
        if self.take_mean:
            self._plot_mean(column)
            return
        for car, data in self.enabled_cars.items():
            plt.plot(data[column], label=car)
        plt.legend()

    def _plot_mean(self, column: str = "position") -> None:
        data = self.mean()
        plt.plot(data[column], label="mean")


class DoublePlotter(CarPlotter):
    def __init__(
        self,
        cars_1: dict[str, pd.DataFrame],
        cars_2: dict[str, pd.DataFrame],
    ) -> None:
        super().__init__(cars_1)
        self.cars_2 = cars_2

    @property
    def enabled_cars_2(self) -> dict[str, pd.DataFrame]:
        return {car: data for car, data in self.cars_2.items() if car not in self.disabled_ids}

    def mean2(self) -> pd.DataFrame:
        return pd.concat(self.enabled_cars_2.values()).groupby(level=0).mean()

    def plot(self, column: str = "position") -> None:
        if self.take_mean:
            self._plot_mean(column)
            return

        color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])
        for car in self.enabled_cars:
            color = next(color_cycle)
            plt.plot(self.cars[car][column], label=f"{car} 1", color=color)
            plt.plot(self.cars_2[car][column], label=f"{car} 2", color=color, linestyle=":", alpha=0.7)

        plt.legend()
        plt.show()

    def _plot_mean(self, column: str = "position") -> None:
        data = self.mean()
        plt.plot(data[column], color="#1f77b4")
        data = self.mean2()
        plt.plot(data[column], color="#1f77b4", linestyle=":", alpha=0.7)
        plt.show()


class TUI:
    def __init__(self, plotter: CarPlotter) -> None:
        self.plotter = plotter

    def home_screen(self) -> None:
        print("DRIVE Plotter")
        if self.plotter.enabled_cars:
            print("Enabled: ")
            print(", ".join(sorted(self.plotter.enabled_cars.keys())))
        if self.plotter.disabled_ids:
            print("Disabled: ")
            print(", ".join(sorted(self.plotter.disabled_ids)))

        print("Mean is", "enabled" if self.plotter.take_mean else "disabled")
        print("Options:")
        print("(P)lot, (E)nable, (D)isable, (M)ean, (Q)uit")
        option = input(">>> ").casefold()
        match option:
            case "p":
                return self.plot()
            case "e":
                return self.enable()
            case "d":
                return self.disable()
            case "m":
                self.plotter.take_mean = not self.plotter.take_mean
                return self.home_screen()
            case "q":
                return
            case _:
                return self.home_screen()

    def plot(self) -> None:
        options = sorted(list(self.plotter.enabled_cars.values())[0].columns)
        mapped_options = {option[0]: option for option in options}
        options = [f"({option[0].upper()})" + option[1:] for option in options]
        print("Options:")
        print(", ".join(options))
        option = input(">>> ").casefold()
        try:
            self.plotter.plot(mapped_options[option])
        except KeyError:
            print("Invalid option")
            return self.plot()
        plt.show()
        return self.home_screen()

    def enable(self) -> None:
        cars = input("(A)ll, or comma separated list: ").casefold().split(",")
        if "a" in cars:
            self.plotter.enable_all()
            return self.home_screen()
        for car in cars:
            try:
                self.plotter.enable_car(car)
            except KeyError:
                print(f"Car {car} not found")
        return self.home_screen()

    def disable(self) -> None:
        cars = input("(A)ll, or comma separated list: ").casefold().replace(" ", "").split(",")
        if "a" in cars:
            self.plotter.disable_all()
            return self.home_screen()
        for car in cars:
            try:
                self.plotter.disable_car(car)
            except KeyError:
                print(f"Car {car} not found")
        return self.home_screen()


def main():
    assert 1 < len(argv) < 4, "Please provide only one or two file paths"
    cars_1 = load_data(argv[1])
    cars_2 = None
    if len(argv) == 3:
        cars_2 = load_data(argv[2])

    if cars_2:
        assert cars_1.keys() == cars_2.keys(), "Both files must have the same cars\n"\
            f"First: {list(cars_1.keys())}\n"\
            f"Second: {list(cars_2.keys())}"

    if cars_2:
        plotter = DoublePlotter(cars_1, cars_2)
    else:
        plotter = CarPlotter(cars_1)

    tui = TUI(plotter)
    try:
        tui.home_screen()
    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    main()
