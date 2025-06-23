import time
import datetime

# --- Base Class for Smart Devices ---
class SmartDevice:
    """Base class for all smart home devices."""
    def __init__(self, name):
        self.name = name
        self.is_on = False # Common state for many devices (e.g., power)

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print(f"[{self.name}] turned ON.")
        else:
            print(f"[{self.name}] is already ON.")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print(f"[{self.name}] turned OFF.")
        else:
            print(f"[{self.name}] is already OFF.")

    def get_status(self):
        status = "ON" if self.is_on else "OFF"
        return f"{self.name}: {status}"

# --- Specific Device Classes ---

class SmartLight(SmartDevice):
    """Represents a smart light."""
    def __init__(self, name, brightness=50):
        super().__init__(name)
        self.brightness = brightness # 0-100
    
    def set_brightness(self, level):
        if 0 <= level <= 100:
            self.brightness = level
            if level > 0 and not self.is_on:
                self.turn_on() # Turn on if setting brightness > 0
            elif level == 0 and self.is_on:
                self.turn_off() # Turn off if setting brightness to 0
            print(f"[{self.name}] brightness set to {self.brightness}%.")
        else:
            print(f"[{self.name}] Invalid brightness level. Must be 0-100.")

    def get_status(self):
        status = super().get_status()
        return f"{status}, Brightness: {self.brightness}%"

class SmartThermostat(SmartDevice):
    """Represents a smart thermostat."""
    def __init__(self, name, current_temp=22, target_temp=20):
        super().__init__(name)
        self.current_temp = current_temp
        self.target_temp = target_temp
        self.mode = "Off" # Off, Heating, Cooling
    
    def set_target_temp(self, temp):
        if 10 <= temp <= 30: # Reasonable temperature range
            self.target_temp = temp
            print(f"[{self.name}] target temperature set to {self.target_temp}°C.")
            self._update_mode()
        else:
            print(f"[{self.name}] Invalid target temperature. Must be 10-30°C.")

    def _update_mode(self):
        """Simulate heating/cooling based on current vs target temp."""
        if self.is_on:
            if self.current_temp < self.target_temp - 1: # Small buffer
                self.mode = "Heating"
                print(f"[{self.name}] Mode: Heating (Current: {self.current_temp}°C, Target: {self.target_temp}°C)")
            elif self.current_temp > self.target_temp + 1:
                self.mode = "Cooling"
                print(f"[{self.name}] Mode: Cooling (Current: {self.current_temp}°C, Target: {self.target_temp}°C)")
            else:
                self.mode = "Idle"
                print(f"[{self.name}] Mode: Idle (Current: {self.current_temp}°C, Target: {self.target_temp}°C)")
        else:
            self.mode = "Off"

    def turn_on(self):
        super().turn_on()
        self._update_mode()

    def turn_off(self):
        super().turn_off()
        self.mode = "Off"
        print(f"[{self.name}] Thermostat turned OFF.")

    def get_status(self):
        status = super().get_status()
        return f"{status}, Current: {self.current_temp}°C, Target: {self.target_temp}°C, Mode: {self.mode}"

class SmartDoorLock(SmartDevice):
    """Represents a smart door lock."""
    def __init__(self, name, is_locked=True):
        super().__init__(name)
        self.is_locked = is_locked
        self.is_on = True # A lock is always 'on' in terms of power, just its state changes

    def lock(self):
        if not self.is_locked:
            self.is_locked = True
            print(f"[{self.name}] Door LOCKED.")
        else:
            print(f"[{self.name}] Door is already LOCKED.")

    def unlock(self):
        if self.is_locked:
            self.is_locked = False
            print(f"[{self.name}] Door UNLOCKED.")
        else:
            print(f"[{self.name}] Door is already UNLOCKED.")

    def get_status(self):
        status = "LOCKED" if self.is_locked else "UNLOCKED"
        return f"{self.name}: {status}"

    # Override base class methods as power state doesn't apply directly
    def turn_on(self):
        print(f"[{self.name}] Lock power is always on.")
    def turn_off(self):
        print(f"[{self.name}] Lock power cannot be turned off (it's always ready).")


# --- Smart Home Hub ---
class SmartHomeHub:
    """Manages all smart devices and automation rules."""
    def __init__(self):
        self.devices = {}
        self.simulated_time = datetime.datetime.now().replace(second=0, microsecond=0) # Start with current time
        print(f"Smart Home Hub initialized. Current simulated time: {self.simulated_time.strftime('%H:%M')}")

    def add_device(self, device):
        self.devices[device.name.lower()] = device
        print(f"Added device: {device.name}")

    def get_device(self, name):
        return self.devices.get(name.lower())

    def list_devices(self):
        if not self.devices:
            print("No devices added to the hub.")
            return

        print("\n--- Device Status ---")
        for device_name, device_obj in self.devices.items():
            print(device_obj.get_status())
        print("---------------------")

    def advance_time(self, minutes):
        """Simulates advancing time for automation testing."""
        self.simulated_time += datetime.timedelta(minutes=minutes)
        print(f"\nSimulated time advanced by {minutes} minutes. New time: {self.simulated_time.strftime('%H:%M')}")
        self.run_automation_rules() # Check rules after time advance

    def set_simulated_time(self, hour, minute):
        """Sets the simulated time to a specific hour and minute today."""
        now = datetime.datetime.now()
        try:
            new_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            self.simulated_time = new_time
            print(f"\nSimulated time set to: {self.simulated_time.strftime('%H:%M')}")
            self.run_automation_rules() # Check rules after time set
        except ValueError:
            print("Invalid hour or minute. Hour must be 0-23, minute 0-59.")

    def run_automation_rules(self):
        """Checks and executes defined automation rules."""
        print("\n--- Running Automation Rules ---")
        current_hour = self.simulated_time.hour
        current_minute = self.simulated_time.minute

        # Rule 1: Turn off living room lights at 23:00 (11 PM)
        living_room_light = self.get_device("Living Room Light")
        if living_room_light and current_hour == 23 and current_minute == 0 and living_room_light.is_on:
            print("[AUTOMATION] It's 23:00. Turning off Living Room Light.")
            living_room_light.turn_off()

        # Rule 2: Turn on front door light at 18:00 (6 PM) if it's off
        front_door_light = self.get_device("Front Door Light")
        if front_door_light and current_hour == 18 and current_minute == 0 and not front_door_light.is_on:
            print("[AUTOMATION] It's 18:00. Turning on Front Door Light.")
            front_door_light.turn_on()

        # Rule 3: Lock Front Door at 22:00 (10 PM)
        front_door_lock = self.get_device("Front Door Lock")
        if front_door_lock and current_hour == 22 and current_minute == 0 and not front_door_lock.is_locked:
            print("[AUTOMATION] It's 22:00. Locking Front Door.")
            front_door_lock.lock()
        
        # Rule 4: Adjust thermostat based on simulated temperature changes
        thermostat = self.get_device("Main Thermostat")
        if thermostat and thermostat.is_on:
             # Simulate temperature changing over time, very basic
            if thermostat.mode == "Heating":
                if thermostat.current_temp < thermostat.target_temp:
                    thermostat.current_temp += 0.5 # Slowly increase temp
                    print(f"[{thermostat.name}] Simulated temp rise to {thermostat.current_temp}°C.")
            elif thermostat.mode == "Cooling":
                 if thermostat.current_temp > thermostat.target_temp:
                    thermostat.current_temp -= 0.5 # Slowly decrease temp
                    print(f"[{thermostat.name}] Simulated temp drop to {thermostat.current_temp}°C.")
            thermostat._update_mode() # Re-evaluate mode after temp change
        print("--- Automation Rules Check Complete ---")

# --- Main Interaction Loop ---

def display_menu():
    """Displays the main menu options."""
    print("\n--- Smart Home Control Menu ---")
    print("1. List All Devices")
    print("2. Control a Device")
    print("3. Advance Simulated Time")
    print("4. Set Simulated Time")
    print("5. Run Automation Rules Now")
    print("6. Exit")
    print("-----------------------------")

def control_device_menu(hub):
    """Menu for controlling individual devices."""
    device_name = input("Enter device name (e.g., Living Room Light): ").strip()
    device = hub.get_device(device_name)

    if not device:
        print(f"Device '{device_name}' not found.")
        return

    print(f"\n--- Controlling {device.name} ---")
    print(f"Current Status: {device.get_status()}")

    if isinstance(device, SmartLight):
        action = input("Enter action (on/off/brightness/status): ").lower().strip()
        if action == "on":
            device.turn_on()
        elif action == "off":
            device.turn_off()
        elif action == "brightness":
            try:
                level = int(input("Enter brightness level (0-100): "))
                device.set_brightness(level)
            except ValueError:
                print("Invalid brightness level.")
        elif action == "status":
            print(device.get_status())
        else:
            print("Invalid action for light.")
    elif isinstance(device, SmartThermostat):
        action = input("Enter action (on/off/set_temp/status): ").lower().strip()
        if action == "on":
            device.turn_on()
        elif action == "off":
            device.turn_off()
        elif action == "set_temp":
            try:
                temp = int(input("Enter target temperature (10-30°C): "))
                device.set_target_temp(temp)
            except ValueError:
                print("Invalid temperature.")
        elif action == "status":
            print(device.get_status())
        else:
            print("Invalid action for thermostat.")
    elif isinstance(device, SmartDoorLock):
        action = input("Enter action (lock/unlock/status): ").lower().strip()
        if action == "lock":
            device.lock()
        elif action == "unlock":
            device.unlock()
        elif action == "status":
            print(device.get_status())
        else:
            print("Invalid action for door lock.")
    else:
        # Generic on/off for other future devices
        action = input("Enter action (on/off/status): ").lower().strip()
        if action == "on":
            device.turn_on()
        elif action == "off":
            device.turn_off()
        elif action == "status":
            print(device.get_status())
        else:
            print("Invalid action.")

    print(f"New Status: {device.get_status()}")


def main():
    hub = SmartHomeHub()

    # Add some simulated devices to the hub
    hub.add_device(SmartLight("Living Room Light"))
    hub.add_device(SmartLight("Bedroom Light", brightness=75))
    hub.add_device(SmartThermostat("Main Thermostat", current_temp=25, target_temp=22))
    hub.add_device(SmartDoorLock("Front Door Lock"))
    hub.add_device(SmartLight("Front Door Light", brightness=0)) # Initially off

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            hub.list_devices()
        elif choice == '2':
            control_device_menu(hub)
        elif choice == '3':
            try:
                minutes = int(input("Enter minutes to advance time by: "))
                hub.advance_time(minutes)
            except ValueError:
                print("Invalid input. Please enter a number for minutes.")
        elif choice == '4':
            try:
                time_str = input("Enter new simulated time (HH:MM, e.g., 22:00): ")
                hour, minute = map(int, time_str.split(':'))
                hub.set_simulated_time(hour, minute)
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
        elif choice == '5':
            hub.run_automation_rules()
        elif choice == '6':
            print("Exiting Smart Home Control. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        time.sleep(0.5) # Short pause for readability in console

if __name__ == "__main__":
    main()