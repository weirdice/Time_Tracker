"""Module runs a time tracking app"""

import pickle
from dataclasses import dataclass
from typing import Optional


@dataclass
class SaveData:
    """Class for tracking user settings and current timestamps"""

    round_min: int
    goal_time: float
    time_records: Optional[dict] = None


def load_data() -> SaveData:
    """Function that loads user data. If no user data is found or format is unexpected save default data file"""
    try:
        with open("savestate", "rb") as f:
            temp_data = pickle.load(f)
            if not isinstance(temp_data, SaveData):
                temp_data = SaveData(round_min=15, goal_time=8)
                save_data(temp_data)

    except FileNotFoundError:
        temp_data = SaveData(round_min=15, goal_time=8)
        save_data(temp_data)
    return temp_data


def save_data(current_data: SaveData) -> None:
    """Function to save user data to binary file"""
    with open("savestate", "wb") as f:
        pickle.dump(current_data, f)


def main():
    """main function"""
    current_data = load_data()
    print(current_data)


if __name__ == "__main__":
    main()
