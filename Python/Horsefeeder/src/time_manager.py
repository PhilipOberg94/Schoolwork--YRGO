import time
from datetime import datetime
import subprocess

class TimeManager:
    def __init__(self):
        # Check if RTC is available as a system device
        try:
            subprocess.run(["hwclock", "--show"], check=True, capture_output=True)
            self.rtc_available = True
            print("System RTC (DS3231) detected")
        except subprocess.CalledProcessError as e:
            self.rtc_available = False
            print(f"No system RTC detected, using system time only: {e}")

    def get_time(self):
        """Get the current time from the system (synced with DS3231 via hwclock)."""
        current_time = datetime.fromtimestamp(time.time())
        return current_time.strftime('%H:%M')

    def set_time(self, new_time_struct):
        """Set system and RTC time using a time.struct_time object."""
        if self.rtc_available:
            try:
                # Convert time.struct_time to a string for date command
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', new_time_struct)
                # Set system time (requires sudo)
                subprocess.run(["sudo", "date", "-s", time_str], check=True)
                # Sync system time to hardware clock (DS3231)
                subprocess.run(["sudo", "hwclock", "--systohc"], check=True)
                print(f"RTC time set to: {time_str}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to set RTC time: {e}")
        else:
            print("No RTC available, cannot set time")

    def set_system_time(self, new_time_str):
        """Set system and RTC time using a string (e.g., '2025-03-28 14:30:00')."""
        if self.rtc_available:
            try:
                # Set system time directly with string (requires sudo)
                subprocess.run(["sudo", "date", "-s", new_time_str], check=True)
                # Sync to hardware clock
                subprocess.run(["sudo", "hwclock", "--systohc"], check=True)
                print(f"System and RTC time set to: {new_time_str}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to set system/RTC time: {e}")
                return 1  # Error code
            return 0  # Success code
        else:
            print("No RTC available, cannot set time")
            return 1  # Error code

    def sync_with_system(self):
        """Sync RTC with current system time."""
        if self.rtc_available:
            self.set_time(time.localtime())

    def compare_time(self, box_time):
        """Check if the current time matches the box open time."""
        current_time = self.get_time()
        return 1 if current_time == box_time else 0

# Test the class
if __name__ == "__main__":
    tm = TimeManager()
    print("Current time:", tm.get_time())
    # Test comparing time
    test_box_time = "14:30"  # Example time to compare
    print(f"Does {tm.get_time()} match {test_box_time}? {tm.compare_time(test_box_time)}")
    # Optional: Sync RTC with system time (requires sudo)
    print("Syncing RTC with system time...")
    tm.sync_with_system()
    print("Updated time:", tm.get_time())
    # Optional: Set a specific time (requires sudo)
    new_time = "2025-03-28 15:45:00"
    print(f"Setting time to {new_time}...")
    tm.set_system_time(new_time)
    print("New time:", tm.get_time())