"""Module runs a time tracking app"""

import pickle
from dataclasses import dataclass
from time import sleep, time


@dataclass
class SaveData:
    """Class for tracking user settings and current timestamps"""

    round_min: int
    goal_time: float
    tracking_active: bool
    time_records: dict[int, str]


def load_data() -> SaveData:
    """Overrides current_data with saved data if available. Otherwise saves current_data"""
    try:
        with open("save_state", "rb") as f:
            temp_data = pickle.load(f)
            if not isinstance(temp_data, SaveData):
                temp_data = SaveData(
                    round_min=15, goal_time=8, tracking_active=False, time_records={}
                )
                save_data(temp_data)

    except FileNotFoundError:
        temp_data = SaveData(
            round_min=15, goal_time=8, tracking_active=False, time_records={}
        )
        save_data(temp_data)
    return temp_data


def save_data(data: SaveData) -> None:
    """Function to save user data to binary file"""
    with open("save_state", "wb") as f:
        pickle.dump(data, f)


def add_timestamp(task_name: str, data: SaveData) -> SaveData:
    """Adds a value to the time_record dictionary for the current time and
    given task name and saves updated user data"""
    data.time_records[int(time())] = task_name
    save_data(data)
    return data


def calculate_timings(data: SaveData) -> tuple[int, list[tuple[str, int]], int]:
    """Uses SaveData object to return:
    total time spent on tasks, duration for each task, and time spent on breaks"""
    timestamp_list = list(data.time_records.keys())
    duration_list = [
        (data.time_records[x], (y - x))
        for x, y in zip(timestamp_list, timestamp_list[1:])
    ]
    break_time = sum(v[1] for v in duration_list if v[0] == "BREAK")
    total_time = (timestamp_list[-1] - timestamp_list[0]) - break_time
    duration_list = [x for x in duration_list if x[0] != "BREAK"]
    return (total_time, duration_list, break_time)


def main():
    """main function"""
    current_data = SaveData(
        round_min=15, goal_time=8, tracking_active=False, time_records={}
    )  # load_data()
    current_data = add_timestamp(input("type something: "), current_data)
    sleep(30)
    current_data = add_timestamp("BREAK", current_data)
    sleep(45)
    current_data = add_timestamp(input("type something else: "), current_data)
    sleep(50)
    current_data = add_timestamp(input("type something else: "), current_data)

    print(calculate_timings(current_data))


if __name__ == "__main__":
    main()
