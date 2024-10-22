import time
import board
import busio
import adafruit_ds1307  # Assuming you're using the DS1307 RTC
from datetime import datetime  # Corrected import statement

class RTC:
    def __init__(self):
        # Setup I2C connection
        i2c = busio.I2C(board.SCL, board.SDA)
        self.rtc = adafruit_ds1307.DS1307(i2c)

    def get_time(self):
        # Get the current time from the RTC
        if self.rtc.datetime is not None:
            current_time_struct = self.rtc.datetime
            current_time = datetime.fromtimestamp(time.mktime(current_time_struct))
            
            formatted_time = current_time.strftime('%H:%M')
            # Convert datetime to time.struct_time
            return formatted_time
        else:
            print("RTC not connected")
            return time.localtime()
            

    def set_time(self, new_time):
        # Convert time.struct_time to datetime
        new_datetime = datetime.fromtimestamp(time.mktime(new_time))
        # Set the RTC time (manually set the date/time)
        self.rtc.datetime = new_datetime