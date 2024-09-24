from lcd_controller import LCDController
from time_manager import TimeManager
from box_manager import BoxManager
from button import ButtonManager

class HorseFeeder:
    def __init__(self):
        self.lcd = LCDController()
        self.time_manager = TimeManager()
        self.box_manager = BoxManager()
        self.button_manager = ButtonManager()
        self.menu_int = 1

    def display_menu(self):
        current_time = self.time_manager.get_current_time()
        hour, minute = current_time.hour, current_time.minute
        message = f"Box {self.menu_int}: {hour:02}:{minute:02}"
        self.lcd.display_message(message)

    def navigate_menu(self):
        button_value = self.button_manager.read_button()
        
        if button_value == 'up':
            self.menu_int += 1
        elif button_value == 'down':
            self.menu_int -= 1

        if self.menu_int > 4:
            self.menu_int = 1
        if self.menu_int < 1:
            self.menu_int = 4

    def run(self):
        while True:
            self.display_menu()
            self.navigate_menu()
