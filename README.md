# Time Tracking App

Goal of this project is to create an app for tracking time spent on multiple tasks and then give aggregate times rounded to the nearest n minutes at the end.

*Base functionality of app complete but working in terminal without a GUI*

### Learning Goals:

- Making a GUI with python
- Implementing User Data

## MAIN SCREENS
- [ ] Start / Summary Screen
    - Includes Button to restart for new day
    - Includes a summary of previous workday times
- [ ] Working Screen
    - Buttons Needed: "Take a Break", "End Day" and "Start new Task"
    - Background visual to show passage of time *hourglass*?
- [ ] New Task Screen
    - Includes dynamic buttons for tasks started that day
    - Includes default option to write in a task
- [ ] Break Screen
    - Buttons needed: "End Day" and "Start new Task"
- [ ] Setting Screen / *overlay*?
    - Options for rounding time: 1min, 5min, 10min, 15min
    - Goal setting: desired work per day
    - Testing mode: *counts seconds instead of minutes*

## BACKGROUND FEATURES
- [x] Saving data for settings
- [x] Saving log for current day
- [x] Rounding algorithm for rounding **total** time up and then rounding task times to sum to rounded total.
- [x] System for recovery if app is closed mid-day