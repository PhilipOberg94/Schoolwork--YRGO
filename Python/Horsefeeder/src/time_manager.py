from rtc import RTC
from datetime import datetime

class TimeManager:
    def __init__(self):
        self.rtc = RTC()

    def get_current_time(self):
        # Get current time from the RTC module
        return self.rtc.get_time()

    def set_system_time(self, new_time):
        # Set the time to a specific value
        self.rtc.set_time(new_time)
