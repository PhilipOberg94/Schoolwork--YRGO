import digitalio
import board

class ButtonManager:
    def __init__(self):
        self.button_inc = digitalio.DigitalInOut(board.D6)
        self.button_inc.direction = digitalio.Direction.INPUT
        self.button_inc.pull = digitalio.Pull.UP

        self.button_dec = digitalio.DigitalInOut(board.D5)
        self.button_dec.direction = digitalio.Direction.INPUT
        self.button_dec.pull = digitalio.Pull.UP

    def is_increment_pressed(self):
        """Returns True if the increment button is pressed."""
        return not self.button_inc.value  # Button is active-low

    def is_decrement_pressed(self):
        """Returns True if the decrement button is pressed."""
        return not self.button_dec.value  # Button is active-low
