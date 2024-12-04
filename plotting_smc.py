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
            "accel: [1, 2, 3, 4, 5]
        },
        "55": {
            "speed": [1, 2, 3, 4, 5],
            "position": [1, 2, 3, 4, 5]
            "accel": [1, 2, 3, 4, 5]
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
    drive_cars_without = load_data("data_without.json")
    data_30 = load_data("data_1.0.json")
    data_31 = load_data("data_1.1.json")
    data_32 = load_data("data_1.2.json")
    data_33 = load_data("data_1.3.json")
    data_34 = load_data("data_1.4.json")
    data_35 = load_data("data_1.5.json")
    data_36 = load_data("data_1.6.json")
    data_37 = load_data("data_1.7.json")
    data_38 = load_data("data_1.8.json")
    data_39 = load_data("data_1.9.json")
    data_40 = load_data("data_2.0.json")
    data_41 = load_data("data_2.1.json")
    data_42 = load_data("data_2.2.json")
    data_43 = load_data("data_2.3.json")
    data_44 = load_data("data_2.4.json")
    data_45 = load_data("data_2.5.json")

    carposition = "140"

    datasets = [data_30, data_31, data_32, data_33, data_34, data_35, data_36, data_37, data_38, data_39, data_40, data_41, data_42, data_43, data_44, data_45]
    adoption_rates = [1.0 + 0.1 * i for i in range(16)]
    effectiveness = []

    for data in datasets:
        effectiveness_car = (data[carposition]['position'].iloc[-1] - drive_cars_without[carposition]['position'].iloc[-1]) / (drive_cars_without[carposition]['position'].iloc[-1]) * 100
        print(effectiveness_car)
        effectiveness.append(effectiveness_car)

    plt.plot(adoption_rates, effectiveness, marker='o')
    plt.xlabel('Adoption Rate')
    plt.ylabel('Effectiveness (%)')
    plt.title('Effectiveness vs Adoption Rate')
    plt.grid(True)
    plt.savefig('effectiveness_vs_adoption_rate.png')
    plt.show()



    #drive_effectiveness1 = (drive_cars_drive1[carposition]['position'].iloc[-1] - drive_cars_without[carposition]['position'].iloc[-1]) / drive_cars_without[carposition]['position'].iloc[-1] * 100
    #drive_effectiveness2 = (drive_cars_drive2[carposition]['position'].iloc[-1] - drive_cars_without[carposition]['position'].iloc[-1]) / drive_cars_without[carposition]['position'].iloc[-1] * 100
    #print(f"Drive effectiveness drive 1: {drive_effectiveness1:.2f}%")
    #print(f"Drive effectiveness drive 2: {drive_effectiveness2:.2f}%")


    #  for car, data in data_30.items():
    #      plt.plot(data["speed"], label=car)
    #  plt.show()


if __name__ == "__main__":
    main()


