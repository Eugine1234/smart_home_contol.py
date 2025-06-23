# smart_home_contol.py
# Python Simulated Smart Home Control

A simple, text-based Python application that simulates controlling various smart home devices and implements basic automation rules.

## Features:
- Simulate Smart Lights (On/Off, Brightness)
- Simulate Smart Thermostat (On/Off, Target Temperature, Heating/Cooling Modes)
- Simulate Smart Door Lock (Lock/Unlock)
- Time-based Automation Rules (e.g., lights off at 23:00, door locks at 22:00)
- Interactive menu for manual control and time manipulation.

## How to Run:
1.  **Prerequisites:**
    - Python 3.x installed on your system.

2.  **Save the Code:**
    - Save the `smart_home_control.py` file into a directory on your computer.

3.  **Run from VS Code Terminal:**
    - Open your project folder in VS Code.
    - Open the integrated terminal (`Ctrl + ` `` ` ``).
    - Run the script using:
        ```bash
        python smart_home_control.py
        ```

## Usage:
The program will present an interactive menu in the terminal.
- `1`: List all simulated devices and their current status.
- `2`: Control a specific device (e.g., turn a light on/off, set thermostat temp).
- `3`: Advance simulated time by a number of minutes to test automation.
- `4`: Set simulated time to a specific HH:MM.
- `5`: Manually run automation rules check.
- `6`: Exit the program.

## Example Automation Rules:
(These are hardcoded in the `run_automation_rules` function within the script)
- Living Room Light turns OFF at 23:00.
- Front Door Light turns ON at 18:00.
- Front Door Lock is LOCKED at 22:00.
- Thermostat adjusts simulated temperature based on its heating/cooling mode.

---
*This is a simulated project and does not interact with real smart home hardware.*
