from i2c_lcd import I2CLCD
from button import ButtonManager
from relay_control import RelayControl
from box_manager import BoxManager
from time_manager import TimeManager
import time

class HorseFeeder:
    def __init__(self):
        self.lcd = I2CLCD()  # Use the new I2C-based LCD
        self.buttons = ButtonManager()
        self.box_manager = BoxManager()
        self.relay_control = RelayControl(self.box_manager)
        self.time_manager = TimeManager()

    def run(self):
        """Main loop to check the time, handle buttons, and activate relay."""
        try:
            while True:
                # Get the current time and box time
                current_time = self.time_manager.get_current_time()
                box_time = self.box_manager.get_boxtime()

                # Handle button presses
                if self.buttons.is_increment_pressed():
                    self.box_manager.increment_boxtime()
                    time.sleep(0.5)  # Debounce

                if self.buttons.is_decrement_pressed():
                    self.box_manager.decrement_boxtime()
                    time.sleep(0.5)  # Debounce

                # Check if it's time to open the box
                if self.time_manager.compare_time(current_time, box_time):
                    self.relay_control.activate_solenoid(1)

                # Display current time and box time on the LCD
                self.lcd.display_message(f"Time: {current_time}", 1)

                time.sleep(1)
                
                self.lcd.display_message(f"Box 1&2: {box_time}", 2)

                time.sleep(1)

        except KeyboardInterrupt:
            self.lcd.clear()
            print("Program stopped by user.")