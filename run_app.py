"""Module runs a time tracking app"""

import pickle
from dataclasses import dataclass
from time import time


@dataclass
class SaveData:
    """Class for tracking user settings and current timestamps"""

    round_min: int
    goal_time: float
    tracking_active: bool
    time_records: dict


def load_data() -> SaveData:
    """Function that loads user data. If no user data is found or format is unexpected save default data file"""
    try:
        with open("savestate", "rb") as f:
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


def save_data(current_data: SaveData) -> None:
    """Function to save user data to binary file"""
    with open("savestate", "wb") as f:
        pickle.dump(current_data, f)


def add_timestamp(task_name: str, current_data: SaveData) -> None:
    """Adds a value to the time_record dictionary for the current time and given task name and saves updated user data"""
    current_data.time_records[time()] = task_name
    save_data(current_data)


def main():
    """main function"""
    current_data = load_data()
    add_timestamp(input("type something: "), current_data)
    add_timestamp(input("type something else: "), current_data)

    print(
        int(
            (
                max(current_data.time_records.keys())
                - min(current_data.time_records.keys())
            )
            // 60
        )
    )
    time_list = list(current_data.time_records.keys())
    print(
        [
            [current_data.time_records[x], y - x]
            for x, y in zip(time_list, time_list[1:])
        ]
    )


if __name__ == "__main__":
    main()
