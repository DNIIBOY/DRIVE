from pathlib import Path
from matplotlib import pyplot as pltz
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
    #print(file_path)
    with open(file_path, "r") as file:
        data = json.load(file)

    for car, values in data.items():
        for key, value in values.items():
            values[key] = np.array(value)
        del values["id"]
        cars[car] = pd.DataFrame(values)
    return cars

def calculate_average(data):
    result = {}
    for car in data[0]:
        result[car] = pd.concat([df[car] for df in data]).groupby(level=0).mean()
    return result


def generate_average_jsonfile(statistic: str, step: float):
    import os
    from os.path import exists
    data_dir = Path("data/")
    all_data_files = sorted(data_dir.glob("*.json"))
    all_data = [load_data(file) for file in all_data_files]
    average_data = calculate_average(all_data)
    step = float(step)
    formatted_step = f"{step:.3f}"
    print(formatted_step)
    filename = f"avg_{statistic}_{formatted_step}_"

    output_file = f"avg_data/{filename}"
    average_data_to_save = {}
    for car, df in average_data.items():
        average_data_to_save[car] = df.to_dict(orient="list")
        average_data_to_save[car]["id"] = car

    while exists(f"{output_file}.json"):
        filename += "1"
        output_file = f"avg_data/{filename}"



    with open(f"{output_file}.json", "w") as file:
        json.dump(average_data_to_save, file, indent=4)
    for file in all_data_files:
       os.remove(file)

if __name__ == "__main__":
    generate_average_jsonfile("headway_factor", 0.1)


