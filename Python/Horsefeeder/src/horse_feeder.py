import i2c_lcd
import button
import relay_control
import box_manager
import time_manager
import time

class HorseFeeder:
    def __init__(self):
        self.lcd = i2c_lcd.I2CLCD()
        self.buttons = button.ButtonManager()
        self.relay_control = relay_control.RelayControl()
        self.box_manager = box_manager.BoxManager()
        self.time_manager = time_manager.TimeManager()

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
                    self.relay_control.activate_relay()

                # Display current time and box time on the LCD
                self.lcd.display_message(f"Time: {current_time.strftime('%H:%M')}", 1)
                self.lcd.display_message(f"Box 1&2: {box_time[:5]}", 2)

                time.sleep(1)  # Update every second
        except KeyboardInterrupt:
            self.lcd.clear()
            print("Program stopped by user.")
