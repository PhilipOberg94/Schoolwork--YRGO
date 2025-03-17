import time
import board
import busio
import adafruit_ds3231  # Changed from adafruit_ds1307
from datetime import datetime

class RTC:
    def __init__(self):
        try:
            # Setup I2C connection
            i2c = busio.I2C(board.SCL, board.SDA)
            self.rtc = adafruit_ds3231.DS3231(i2c)  # Changed to DS3231
            print("RTC initialized successfully")
        except Exception as e:
            print(f"RTC not found, using system time as fallback: {e}")
            self.rtc = None

    def get_time(self):
        if self.rtc and self.rtc.datetime is not None:
            current_time_struct = self.rtc.datetime
            # Convert time.struct_time to datetime
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

# Test the class
if __name__ == "__main__":
    rtc = RTC()
    print("Current time:", rtc.get_time())
    # Example: Set time to current system time (optional)
    rtc.set_time(time.localtime())
    print("Updated time:", rtc.get_time())
