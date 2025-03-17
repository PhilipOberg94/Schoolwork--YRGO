import time
import board
import busio
import adafruit_ds1307
from datetime import datetime

class RTC:
    def __init__(self):
        try:
            # Setup I2C connection
            i2c = busio.I2C(board.SCL, board.SDA)
            self.rtc = adafruit_ds1307.DS1307(i2c)
            print("RTC initialized successfully")
        except Exception as e:
            print(f"RTC not found, using system time as fallback: {e}")
            self.rtc = None

    def get_time(self):
        if self.rtc and self.rtc.datetime is not None:
            current_time_struct = self.rtc.datetime
            current_time = datetime.fromtimestamp(time.mktime(current_time_struct))
            formatted_time = current_time.strftime('%H:%M')
            return formatted_time
        else:
            # Fallback to system time
            return time.strftime('%H:%M', time.localtime())

    def set_time(self, new_time_struct):
        if self.rtc:
            try:
                self.rtc.datetime = new_time_struct
                print("RTC time set")
            except Exception as e:
                print(f"Failed to set RTC time: {e}")
        else:
            print("No RTC available, cannot set time")