import time
import os
import sys

# from src import button
# from src import relay_control
# from src import box_manager
# from src import time_manager
from src import i2c_lcd
import smbus2
import time

def scan_i2c_bus(bus_number=1):
    bus = smbus2.SMBus(bus_number)
    devices = []
    for address in range(0x03, 0x78):
        try:
            bus.read_byte(address)
            devices.append(hex(address))
        except OSError:
            pass
    bus.close()
    return devices

if __name__ == "__main__":
    print("Scanning I2C bus for devices...")
    devices = scan_i2c_bus()
    if devices:
        print(f"Found I2C devices at addresses: {', '.join(devices)}")
    else:
        print("No I2C devices found.")



sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

scan_i2c_bus()

# # Create an instance of I2CLCD
# lcd = i2c_lcd.I2CLCD()

# lcd.clear()
# # Set LCD color to red
# lcd.set_color(100, 0, 0)
# time.sleep(1)
# # Print two line message
# lcd.display_message("Hello\nCircuitPython")
# # Wait 5s
# time.sleep(5)
# lcd.clear()
# # Print two line message right to left
# lcd.lcd.text_direction = lcd.lcd.RIGHT_TO_LEFT
# lcd.display_message("Hello\nCircuitPython")
# # Wait 5s
# time.sleep(5)
# # Return text direction to left to right
# lcd.lcd.text_direction = lcd.lcd.LEFT_TO_RIGHT
# # Display cursor
# lcd.clear()
# lcd.lcd.cursor = True
# lcd.display_message("Cursor! ")
# # Wait 5s
# time.sleep(5)
# # Display blinking cursor
# lcd.clear()
# lcd.lcd.blink = True
# lcd.display_message("Blinky Cursor!")
# # Wait 5s
# time.sleep(5)
# lcd.lcd.blink = False
# lcd.clear()
# # Create message to scroll
# scroll_msg = "<-- Scroll"
# lcd.display_message(scroll_msg)
# # Scroll to the left
# for i in range(len(scroll_msg)):
#     time.sleep(0.5)
#     lcd.lcd.move_left()
# lcd.clear()
# time.sleep(1)
# lcd.display_message("Going to sleep\nCya later!")
# time.sleep(5)
# # Turn off LCD backlights and clear text
# lcd.set_color(0, 0, 0)
# lcd.clear()