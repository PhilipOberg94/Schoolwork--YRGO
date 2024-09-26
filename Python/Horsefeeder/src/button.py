import board
import digitalio

class ButtonManager:
    def __init__(self):
        # Button pins setup
        self.button_up = digitalio.DigitalInOut(board.D27)
        self.button_down = digitalio.DigitalInOut(board.D23)
        self.button_select = digitalio.DigitalInOut(board.D24)
        
        # Setup input with pull-up resistors
        for button in [self.button_up, self.button_down, self.button_select]:
            button.direction = digitalio.Direction.INPUT
            button.pull = digitalio.Pull.UP

    def read_button(self):
        if not self.button_up.value:
            return 'up'
        if not self.button_down.value:
            return 'down'
        if not self.button_select.value:
            return 'select'
        return None
