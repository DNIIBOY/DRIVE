from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import json


def load_data(file_path: str = "data.json") -> pd.DataFrame:
    """
    Load the data from the JSON file.
    The inner lists will be numpy arrays
    :param file_path: Path to the file
    :return: DataFrame
    {
        "50": {
            "speed": [1, 2, 3, 4, 5],
            "position": [1, 2, 3, 4, 5]
            "acceleration": [1, 2, 3, 4, 5]
        },
        "55": {
            "speed": [1, 2, 3, 4, 5],
            "position": [1, 2, 3, 4, 5]
            "acceleration": [1, 2, 3, 4, 5]
        }
    }
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


class DataPlotter:
    def __init__(
        self,
        plot_dir: str = "plots",
        prefix: str = ""
    ) -> None:
        self.plot_dir = Path(plot_dir)
        self.prefix = prefix

        self.plot_dir.mkdir(exist_ok=True)  # Create the directory, if it doesn't exist

    def _save_plot(self, name: str) -> None:
        """
        Save the plot to the plot directory.
        :param name: Name of the plot
        :return: None
        """
        name = f"{name}.png"
        if self.prefix:
            name = f"{self.prefix}_{name}"

        plt.savefig(self.plot_dir / name)
        plt.close()


def main():
    cars = load_data("data.json")
    for car in cars.values():
        plt.plot(car["speed"])
    plt.show()


if __name__ == "__main__":
    main()
