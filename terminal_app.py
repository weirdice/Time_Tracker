"""Module runs a time tracking app"""

import pickle
from dataclasses import dataclass
from time import time

# Global constants
WELCOME_SCREEN = int(0)
SETTINGS_SCREEN = int(1)
WORK_SCREEN = int(2)
CLOSE_APP = int(3)
DIVISION_VALUE = {True: 1, False: 60}
UNIT_NAME = {True: "seconds", False: "minutes"}


@dataclass
class SaveData:
    """Class for tracking user settings and current timestamps"""

    round_min: int
    goal_time: float
    test_mode: bool
    time_records: dict[int, str]


def save_data(data: SaveData) -> None:
    """Function to save user data to binary file"""
    with open("save_state", "wb") as f:
        pickle.dump(data, f)


def load_data() -> SaveData:
    """Overrides current_data with saved data if available. Otherwise saves current_data"""
    try:
        with open("save_state", "rb") as f:
            temp_data = pickle.load(f)
            if not isinstance(temp_data, SaveData):
                temp_data = SaveData(
                    round_min=15, goal_time=480, test_mode=False, time_records={}
                )
                save_data(temp_data)

    except FileNotFoundError:
        temp_data = SaveData(
            round_min=15, goal_time=480, test_mode=False, time_records={}
        )
        save_data(temp_data)
    return temp_data


def add_timestamp(task_name: str, data: SaveData) -> SaveData:
    """Adds a value to the time_record dictionary for the current time and
    given task name and saves updated user data"""
    data.time_records[int(time())] = task_name
    save_data(data)
    return data


def round_mins(number: int, rounding_value: int) -> int:
    """rounds number to the nearest multiple of rounding_value"""
    return int(number / rounding_value) * rounding_value


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


def summary_timings(data: SaveData) -> tuple[int, list[tuple[str, int]], int]:
    """Calls calculate_timings to get a list of durations.
    Then aggregates like tasks and rounds based on settings"""
    total_time, duration_list, break_time = calculate_timings(data)
    total_time = round_mins(
        total_time // DIVISION_VALUE[data.test_mode], data.round_min
    )
    break_time = round_mins(
        break_time // DIVISION_VALUE[data.test_mode], data.round_min
    )
    task_set = set(x[0] for x in duration_list)
    sum_durations = sorted(
        [
            (
                x,
                sum(y[1] for y in duration_list if y[0] == x)
                // DIVISION_VALUE[data.test_mode],
            )
            for x in task_set
        ],
        key=lambda a: a[1],
        reverse=True,
    )
    remaining_time = total_time
    sum_durations = [
        (x, min(remaining_time, round_mins(y, data.round_min)))
        for x, y in sum_durations
    ]
    return (total_time, sum_durations, break_time)


def get_num(prompt: str) -> float:
    """Converts user input into an int if possible"""
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Incorrect input please type in a number")


def get_bool(prompt: str) -> bool:
    """Translates user input to a boolean if possible"""
    while True:
        try:
            return {"true": True, "yes": True, "false": False, "no": False}[
                input(prompt).lower().strip()
            ]
        except KeyError:
            print("Incorrect input please enter 'true' or 'false'")


def welcome_prompt(data: SaveData) -> tuple[int, SaveData]:
    """Print instructions for navigating main menu and move accordingly"""
    print("Welcome to Time Tracking.")
    print("To reset data type 'RESET'")
    print("To go to the settings menu type 'SETTINGS'")
    print("To get summary of current statistics type 'SUMMARY'")
    print("To close application from any screen type 'QUIT'")
    print("To start working on tasks type a name for the task")
    input_str = input(": ").lower().strip()

    match input_str:
        case "reset":
            return WELCOME_SCREEN, SaveData(
                data.round_min, data.goal_time, data.test_mode, {}
            )
        case "quit":
            return CLOSE_APP, data
        case "settings":
            return SETTINGS_SCREEN, data
        case "summary":
            # Print Summary
            work_time, work_list, break_time = summary_timings(data)
            print(
                f"\nTotal time working: {work_time} {UNIT_NAME[data.test_mode]} \nDetails:"
            )
            for x in work_list:
                print(f"     {x[0]}: {x[1]} {UNIT_NAME[data.test_mode]}")
            print(f"Time on breaks: {break_time} {UNIT_NAME[data.test_mode]}\n")

            return WELCOME_SCREEN, data
        case "break":
            return WORK_SCREEN, add_timestamp("BREAK", data)
        case _:
            return WORK_SCREEN, add_timestamp(input_str, data)


def settings_prompt(data: SaveData) -> tuple[int, SaveData]:
    """Menu for changing app settings"""
    print("Settings:\nto return to main type 'EXIT'")
    print("To update rounding value type 'ROUND'")
    print("To update goal time for work type 'GOAL'")
    print("To turn on or off testing mode type 'TEST'")
    input_str = input(": ").lower().strip()

    match input_str:
        case "test":
            data.test_mode = get_bool("Do you want to set testing to true or false?")
            return SETTINGS_SCREEN, data
        case "exit":
            return WELCOME_SCREEN, data
        case "quit":
            return CLOSE_APP, data
        case "round":
            data.round_min = int(get_num("Input rounding number (min)"))
            return SETTINGS_SCREEN, data
        case "goal":
            data.goal_time = 60 * get_num("Input goal time (hours)")
            return SETTINGS_SCREEN, data
        case _:
            print("ERROR incorrect input")
            return SETTINGS_SCREEN, data


def work_prompt(data: SaveData) -> tuple[int, SaveData]:
    """prompt for tracking time, options are to type a task to start, 'break', or return to main menu"""
    work_time, work_list, break_time = summary_timings(data)
    current_tasks = set(x[0] for x in work_list)
    print(
        f"tracking time {work_time} {UNIT_NAME[data.test_mode]} spent on tasks: {current_tasks} & {break_time} {UNIT_NAME[data.test_mode]} on breaks"
    )
    print("To stop tracking time type 'EXIT'")
    print("To start a break type 'BREAK'")
    print("To start on a new task type name of task")
    input_str = input(": ").lower().strip()

    match input_str:
        case "":
            print("ERROR: no text received\n")
            return WORK_SCREEN, data
        case "exit":
            return WELCOME_SCREEN, add_timestamp("BREAK", data)
        case "quit":
            return CLOSE_APP, data
        case "break":
            return WORK_SCREEN, add_timestamp("BREAK", data)
        case _:
            return WORK_SCREEN, add_timestamp(input_str, data)


def main():
    """main function"""
    current_screen = WELCOME_SCREEN
    current_data = load_data()

    while True:

        if current_screen == WELCOME_SCREEN:
            current_screen, current_data = welcome_prompt(current_data)
        elif current_screen == SETTINGS_SCREEN:
            current_screen, current_data = settings_prompt(current_data)
        elif current_screen == WORK_SCREEN:
            current_screen, current_data = work_prompt(current_data)
        else:
            break


if __name__ == "__main__":
    main()
