# import time
# import os
# import sys
# import smbus2
# import datetime

# sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# from src import horse_feeder, relay_control, box_manager, time_manager, i2c_lcd


# def scan_i2c_bus(bus_number=1):
#     bus = smbus2.SMBus(bus_number)
#     devices = []
#     for address in range(0x03, 0x78):
#         try:
#             bus.read_byte(address)
#             devices.append(hex(address))
#         except OSError:
#             pass
#     bus.close()
#     return devices

# if __name__ == "__main__":
#     print("Scanning I2C bus for devices...")
#     devices = scan_i2c_bus()
#     if devices:
#         print(f"Found I2C devices at addresses: {', '.join(devices)}")
#     else:
#         print("No I2C devices found.")

#     scan_i2c_bus()

#     # Initialize the HorseFeeder class
#     feeder = horse_feeder.HorseFeeder()
#     feeder.run()

import time
import os
import sys
import datetime

# Adjust the path to your source files
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import your custom modules (assuming they exist)
from src import horse_feeder, relay_control, box_manager, time_manager, i2c_lcd

# Optional: If you still need to scan I2C for non-time-related devices (e.g., LCD or relays)
def scan_i2c_bus(bus_number=1):
    try:
        import smbus2
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
    except ImportError:
        print("smbus2 not installed, skipping I2C scan.")
        return []

if __name__ == "__main__":
    # Optional: Scan I2C bus if you still need it for other hardware
    print("Scanning I2C bus for devices...")
    devices = scan_i2c_bus()
    if devices:
        print(f"Found I2C devices at addresses: {', '.join(devices)}")
    else:
        print("No I2C devices found.")

    # Use the system clock (synced via NTP if online)
    current_time = datetime.datetime.now()
    print(f"Current system time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Initialize the HorseFeeder class (assuming it uses time_manager or similar)
    feeder = horse_feeder.HorseFeeder()
    feeder.run()