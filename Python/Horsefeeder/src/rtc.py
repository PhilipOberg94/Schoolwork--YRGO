import time
import board
import busio
import adafruit_ds1307  # Assuming you're using the DS3231 RTC
import datetime

class RTC:
    def __init__(self):
        # Setup I2C connection
        i2c = busio.I2C(board.SCL, board.SDA)
        self.rtc = adafruit_ds1307.DS1307(i2c)

    def get_time(self):
        # Get the current time from the RTC
        if self.rtc.datetime is not None:
            return self.rtc.datetime
        else:
            return datetime.now()

    def set_time(self, datetime):
        # Set the RTC time (manually set the date/time)
        self.rtc.datetime = datetime
