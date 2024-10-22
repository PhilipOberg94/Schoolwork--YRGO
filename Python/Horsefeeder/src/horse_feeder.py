import time
import smbus2
import i2c_lcd, relay_control, rtc, time_manager
from box_manager import BoxManager

class HorseFeeder:
    def __init__(self):
        self.lcd = i2c_lcd.I2CLCD()  # Use the new I2C-based LCD
        self.box_manager = [
           BoxManager("Box 1&2"),
            BoxManager("Box 3&4"),
            BoxManager("Box 5&6"),
            BoxManager("Box 7&8")
        ]
        self.relay_control = relay_control.RelayControl(self.box_manager)
        self.time_manager = time_manager.TimeManager()  # Assuming rtc.RTC() is the class handling RTC
        self.rtc = rtc.RTC()
        self.box_index = 0
        self.last_lcd_update = ["", ""]

    def switch_box(self, direction):
        if direction == "next":
            self.box_index = (self.box_index + 1) % len(self.box_manager)
        elif direction == "previous":
            self.box_index = (self.box_index - 1) % len(self.box_manager)
        print(f"Switched to box {self.box_index + 1}")
        #self.last_lcd_update[0] = ""

    def run(self):
        try:
            while True:
                current_time = self.time_manager.get_current_time()

                for box_index, current_box in enumerate(self.box_manager):
                    box_time = current_box.get_boxtime()
                    if self.time_manager.compare_time(current_time, box_time):
                        self.relay_control.activate_solenoid(box_index + 1)

                current_box = self.box_manager[self.box_index]

                if self.lcd.up_button:
                    current_box.increment_boxtime()
                    print("Up button pressed")
                    time.sleep(0.05)

                if self.lcd.down_button:
                    current_box.decrement_boxtime()
                    print("Down button pressed")
                    time.sleep(0.05)

                if self.lcd.left_button:
                    print("Left button pressed")
                    self.switch_box("previous")
                    time.sleep(0.05)

                if self.lcd.right_button:
                    print("Right button pressed")
                    self.switch_box("next")
                    time.sleep(0.05)

                if self.lcd.select_button:
                    self.rtc.set_time()
                    print("Select button pressed")
                    time.sleep(0.05)

                new_message_box =f"{current_box.box_name}: {current_box.get_boxtime()}"

                if new_message_box != self.last_lcd_update[0]:
                    self.lcd.display_message(new_message_box, 2)
                    self.last_lcd_update[0] = new_message_box
                
                self.lcd.display_message(f"Time: {current_time}", 1)

                time.sleep(0.01)

        except KeyboardInterrupt:
            self.lcd.clear()
            print("Program stopped by user.")

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

# Example usage
if __name__ == "__main__":
    print("Scanning I2C bus for devices...")
    devices = scan_i2c_bus()
    if devices:
        print(f"Found I2C devices at addresses: {', '.join(devices)}")
    else:
        print("No I2C devices found.")

    # Initialize the HorseFeeder class
    feeder = HorseFeeder()
    feeder.run()