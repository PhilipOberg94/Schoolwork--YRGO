import time
import board
import busio
import adafruit_ds3231  # Assuming you're using the DS3231 RTC

class RTC:
    def __init__(self):
        # Setup I2C connection
        i2c = busio.I2C(board.SCL, board.SDA)
        self.rtc = adafruit_ds3231.DS3231(i2c)

    def get_time(self):
        # Get the current time from the RTC
        return self.rtc.datetime

    def set_time(self, datetime):
        # Set the RTC time (manually set the date/time)
        self.rtc.datetime = datetime
