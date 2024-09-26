from i2c_lcd import I2CLCD
from button import ButtonManager
from box_manager import BoxManager
from relay_control import RelayControl
from time_manager import TimeManager
import time

class HorseFeeder:
    def __init__(self):
        self.lcd = I2CLCD()
        self.box_manager = BoxManager()
        self.button_manager = ButtonManager()
        self.relay_control = RelayControl(self.box_manager)
        self.time_manager = TimeManager()

    def display_current_time(self):
        current_time = self.time_manager.get_current_time()
        current_hour = current_time.hour
        current_minute = current_time.minute
        self.lcd.display_message(f"Time: {current_hour:02}:{current_minute:02}")

    def display_box_times(self):
        box1_hour, box1_minute = self.box_manager.get_box_time(1)
        box2_hour, box2_minute = self.box_manager.get_box_time(2)
        self.lcd.display_message(f"B1:{box1_hour:02}:{box1_minute:02} B2:{box2_hour:02}:{box2_minute:02}")

    def navigate_menu(self):
        button_value = self.button_manager.read_button()
        if button_value == 'up':
            # Handle button press (e.g., increase box time)
            pass
        elif button_value == 'down':
            # Handle button press (e.g., decrease box time)
            pass
        elif button_value == 'select':
            # Handle select button (e.g., confirm)
            pass
        time.sleep(0.2)  # Button debounce

    def run(self):
        try:
            while True:
                self.display_current_time()
                self.display_box_times()
                self.relay_control.check_and_open_boxes()
                self.navigate_menu()
                time.sleep(1)
        except KeyboardInterrupt:
            self.lcd.clear()
            self.relay_control.cleanup()
            print("Exiting program...")
