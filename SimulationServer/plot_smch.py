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

    drive_without = load_data("data_normal_long.json")

    drive_ideal = load_data("data_ideal.json")
    
    data_dir = Path("avg_adoption/")
    data_dir_high_res = Path("avg_highres_adoption/")

    all_data_files = sorted(data_dir.glob("*.json"))
    all_data = [load_data(file) for file in all_data_files]

    sorted_cars = sorted(drive_without.keys(), key=lambda x: int(x))

    for car in sorted_cars:
        # Create time index starting from 0 and multiply by 0.05 to get seconds
        time_index = (np.arange(len(drive_without[car]['position'])) * 0.05).tolist()
        car_id = str(int(car) - 5)
        # Plot the positions with the time index
        plt.plot(time_index, drive_without[car]['position'], label=f'Car {car_id}')

    plt.xlabel('Time [s]')
    plt.ylabel('Position [m]')
    plt.title('Car positions over time in stopwave')
    plt.legend()
    plt.show()
    plt.savefig('car_positions_normal_long.png')


    carposition = "95"

    adoption_rates = [float(file.name.split("_")[3]) for file in all_data_files]


    effectiveness = []
    car95_effectivenesslist = []

    # plot all_data distance.
    # for data in all_data:
    #     plt.plot(data[carposition]['position'], label='With CAV')
    # plt.show()


    #print(all_data[5].keys())


    for data in all_data:
        total_effectiveness = 0
        car_count = 0
        for car in data.keys():
            # Calculate the new effectiveness for each car
            ideal_diff = drive_ideal[car]['position'].iloc[-1] - drive_without[car]['position'].iloc[-1]
            data_diff = data[car]['position'].iloc[-1] - drive_without[car]['position'].iloc[-1]
            new_effectiveness_car = (data_diff / ideal_diff) * 100
            
            total_effectiveness += new_effectiveness_car
            car_count += 1
        car95_idealdiff = drive_without[carposition]['position'].iloc[-1] - drive_ideal[carposition]['position'].iloc[-1] # vendt om
        print(car95_idealdiff)
        car95_data_diff = drive_without[carposition]['position'].iloc[-1] - data[carposition]['position'].iloc[-1]
        print(f" data: {car95_data_diff}")
        car95_effectiveness = (car95_data_diff / car95_idealdiff) * 100
        print((car95_data_diff / car95_idealdiff) * 100)
        
        car95_effectivenesslist.append(car95_effectiveness)
        print(f"car 95 effectiveness: {car95_effectiveness}")
        print(f"Average effectiveness: {total_effectiveness / car_count}")
        average_effectiveness = total_effectiveness / car_count
        effectiveness.append(average_effectiveness)



    plt.plot(adoption_rates, car95_effectivenesslist, marker='o')
    plt.xlabel('Adoption rate')
    plt.ylabel('Effectiveness (%)')
    plt.title('Adoption rate vs Effectiveness')
    plt.grid(True)
    plt.savefig('adoption_vs_effectiveness_rate.png')
    plt.show()


    # Plot car position vs effectiveness
    adoption_rate_100_data = all_data[-1]

    car_ids = []
    effectiveness = []
    sorted_car_ids = sorted(adoption_rate_100_data.keys(), key=int)


    for car in sorted_car_ids:
        ideal_diff = drive_ideal[car]['position'].iloc[-1] - drive_without[car]['position'].iloc[-1]
        data_diff = adoption_rate_100_data[car]['position'].iloc[-1] - drive_without[car]['position'].iloc[-1]
        new_effectiveness_car = (data_diff / ideal_diff) * 100
        
        car_ids.append(car)
        effectiveness.append(new_effectiveness_car)

    car_ids = [str(int(car) - 5) for car in car_ids]

    plt.figure()
    plt.plot(car_ids, effectiveness, 'o-', label='Effectiveness at Adoption Rate 1.0')
    plt.xlabel('Number of cars from stopwave source')
    plt.ylabel('Effectiveness (%)')
    plt.title('Car positions vs Effectiveness at Adoption Rate 100%')
    plt.legend()
    plt.grid(True)
    plt.savefig('carpos_optimal_no_PACE.png')
    plt.show()




    # Plot the positions of car 95 in different datasets

    # time skal ganges med 0.05 for at få sekunder
    # position skal ganges med 0.1 for at få meter

    adoption_rate_100_data = all_data[-1]
    adoption_rate_50_data = load_data("avg_adoption/avg_adoption_rate_0.250_.json")
    car_id = "95"
    drive_without_position = drive_without[car_id]['position'][2000:]
    drive_ideal_position = drive_ideal[car_id]['position'][2000:]
    adoption_100_position = adoption_rate_50_data[car_id]['position'][2000:]

    # Create time index starting from 0 and multiply by 0.05 to get seconds
    time_index = (np.arange(len(drive_without_position)) * 0.05).tolist()

    # Multiply positions by 0.1 to get meters
    drive_without_position = [pos * 0.1 for pos in drive_without_position]
    drive_ideal_position = [pos * 0.1 for pos in drive_ideal_position]
    adoption_100_position = [pos * 0.1 for pos in adoption_100_position]

    # Plot the positions
    plt.figure()
    plt.plot(time_index, drive_without_position, label='Regular breaking event')
    plt.plot(time_index, drive_ideal_position, label='No breaking event')
    plt.plot(time_index, adoption_100_position, label='Breaking with PACE - 50% adoption')

    # Highlight the vertical distance at the last time index
    last_time_index = time_index[-1]
    drive_without_end = drive_without_position[-1]
    drive_ideal_end = drive_ideal_position[-1]
    adoption_100_end = adoption_100_position[-1]

    plt.plot(last_time_index, drive_without_end, 'bo') 
    plt.plot(last_time_index, drive_ideal_end, 'ro')    
    plt.plot(last_time_index, adoption_100_end, 'go')  

    plt.vlines(last_time_index, drive_without_end, drive_ideal_end, colors='gray', linestyles='dotted')
    plt.vlines(last_time_index, drive_ideal_end, adoption_100_end, colors='gray', linestyles='dotted')

    orange = drive_ideal_end
    blue = drive_without_end
    green = adoption_100_end


    distance_ideal_adoption = ((orange - green) / (orange - blue)) * 100
    distance_without_ideal = ( (green - blue)/ (orange-blue)) * 100

    plt.text(last_time_index + 3, (drive_without_end + drive_ideal_end) / 2, f'{distance_without_ideal:.0f}%', color='black', bbox=dict(facecolor='white', alpha=1))
    plt.text(last_time_index + 3, (drive_ideal_end + adoption_100_end) / 2, f'{distance_ideal_adoption:.0f}%', color='black', bbox=dict(facecolor='white', alpha=1))

    # Add labels and title
    plt.xlabel('Time [s]')
    plt.ylabel('Position [m]')
    plt.title('Distance traveled by breaking event')
    plt.legend()
    plt.grid(True)
    plt.savefig('car95_position_comparison.png')
    plt.show()


def plot_stats_old():
    drive_brake = load_data("data_normal.json")
    drive_no_brake = load_data("data_ideal.json")

    data_dir = Path("avg_adoption/")
    data_dir_high_res = Path("avg_highres_adoption/")


    all_data_files = sorted(data_dir.glob("*.json"))
    all_data = [load_data(file) for file in all_data_files]
    all_data_high_res_files = sorted(data_dir_high_res.glob("*.json"))
    all_data_high_res = [load_data(file) for file in all_data_high_res_files]

    carposition = "95"

    adoption_rates = [float(file.name.split("_")[3]) for file in all_data_files]
    effectiveness_95 = []


    for data in all_data:
        car95_idealdiff = drive_brake[carposition]['position'].iloc[-1] - drive_no_brake[carposition]['position'].iloc[-1]
        print(car95_idealdiff)
        car95_data_diff = drive_brake[carposition]['position'].iloc[-1] - data[carposition]['position'].iloc[-1]
        print(f" data: {car95_data_diff}")
        car95_effectiveness = (car95_data_diff / car95_idealdiff) * 100
        effectiveness_95.append(car95_effectiveness)
    
    effectiveness_95_highres = []
    adoption_rates_highres = [float(file.name.split("_")[3]) for file in all_data_high_res_files]

    for data in all_data_high_res:
        car95_idealdiff = drive_brake[carposition]['position'].iloc[-1] - drive_no_brake[carposition]['position'].iloc[-1]
        print(car95_idealdiff)
        car95_data_diff = drive_brake[carposition]['position'].iloc[-1] - data[carposition]['position'].iloc[-1]
        print(f" data: {car95_data_diff}")
        car95_effectiveness = (car95_data_diff / car95_idealdiff) * 100
        effectiveness_95_highres.append(car95_effectiveness)



        

    plt.plot(adoption_rates, effectiveness_95, marker='o', label='10 monte carlo runs')
    plt.plot(adoption_rates_highres, effectiveness_95_highres, marker='x', label='100 monte carlo runs')
    plt.xlabel('Adoption rate (%)')
    plt.ylabel('Effectiveness (%)')
    plt.title('Adoption vs Effectiveness')
    plt.legend()
    plt.grid(True)
    plt.savefig('adoption_vs_average_effectiveness_rate.png')
    plt.show()
    




if __name__ == "__main__":
    #generate_average_jsonfile()
    plot_stats_old()
    #plot_statistic_smch()


