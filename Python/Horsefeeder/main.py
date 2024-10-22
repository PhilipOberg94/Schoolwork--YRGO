import time
import os
import sys
import smbus2
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src import horse_feeder, relay_control, box_manager, time_manager, i2c_lcd


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

    scan_i2c_bus()

    # Initialize the HorseFeeder class
    feeder = horse_feeder.HorseFeeder()
    feeder.run()