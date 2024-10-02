from rtc import RTC
from datetime import datetime
import time
import os

class TimeManager:
    def __init__(self):
        self.rtc = RTC()

    def get_current_time(self):
        # Get current time from the RTC module
        rtc_time = self.rtc.get_time()
        return rtc_time
    
    def set_system_time(self, new_time):
        return os.system(f"date -s {new_time}")

    def compare_time(self, current_time, box_time):
        """Check if the current time matches the box open time."""
        if current_time == box_time:
            return 1
        else:
            return 0
    