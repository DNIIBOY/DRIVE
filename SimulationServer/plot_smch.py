from pathlib import Path
from matplotlib import pyplot as plt
from collections import defaultdict
from statistics import mean
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
    print(file_path)
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

def calculate_average(data):
    result = {}
    for car in data[0]:
        result[car] = pd.concat([df[car] for df in data]).groupby(level=0).mean()
    return result


def generate_average_jsonfile():
    import os
    from os.path import exists
    data_dir = Path("data/")
    all_data_files = sorted(data_dir.glob("*.json"))
    all_data = [load_data(file) for file in all_data_files]
    average_data = calculate_average(all_data)

    filename = "average_data"

    output_file = f"avg_data/{filename}_"
    average_data_to_save = {}
    for car, df in average_data.items():
        average_data_to_save[car] = df.to_dict(orient="list")
        average_data_to_save[car]["id"] = car

    name = 0.2

    while exists(f"{output_file}{name:.1f}.json"):
        name += 0.2

    with open(f"{output_file}{name:.1f}.json", "w") as file:
        json.dump(average_data_to_save, file, indent=4)
    for file in all_data_files:
       os.remove(file)

def plot_statistic_smch():

    drive_cars_without = load_data("data_without.json")

    data_dir = Path("avg_data/")

    all_data_files = sorted(data_dir.glob("*.json"))
    all_data = [load_data(file) for file in all_data_files]

    # plot the data
    plt.plot


    carposition = "95"

    adoption_rates = [22 + i * 0.1 for i in range(len(all_data))]
    effectiveness = []

    # plot all_data distance.
    for data in all_data:
        plt.plot(data[carposition]['position'], label='With CAV')
    plt.show()


    for data in all_data:
        total_effectiveness = 0
        car_count = 0
        for car in data.keys():
            effectiveness_car = (data[car]['position'].iloc[-1] - drive_cars_without[car]['position'].iloc[-1]) / (drive_cars_without[car]['position'].iloc[-1]) * 100
            total_effectiveness += effectiveness_car
            car_count += 1
        car_94_effect = (data[carposition]['position'].iloc[-1] - drive_cars_without[car]['position'].iloc[-1]) / (drive_cars_without[car]['position'].iloc[-1]) * 100
        print(f"car 94 effectiveness: {car_94_effect}")
        print(f"Average effectiveness: {total_effectiveness / car_count}")
        average_effectiveness = total_effectiveness / car_count
        effectiveness.append(average_effectiveness)

    plt.plot(adoption_rates, effectiveness, marker='o')
    plt.xlabel('Adoption rate (%)')
    plt.ylabel('Average Effectiveness (%)')
    plt.title('Adoption vs Average Effectiveness')
    plt.grid(True)
    plt.savefig('adoption_vs_average_effectiveness_rate.png')
    plt.show()


if __name__ == "__main__":
    #generate_average_jsonfile()
    plot_statistic_smch()


