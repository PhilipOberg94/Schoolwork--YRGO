import digitalio
import board
import time

class RelayControl:
    def __init__(self, box_manager):
        self.box_manager = box_manager
        self.relays = {
            1: digitalio.DigitalInOut(board.GP0),  # Relay 1
            2: digitalio.DigitalInOut(board.GP1),  # Relay 2
            3: digitalio.DigitalInOut(board.GP2),  # Relay 3
            4: digitalio.DigitalInOut(board.GP3)   # Relay 4
        }
        for relay in self.relays.values():
            relay.direction = digitalio.Direction.OUTPUT
            relay.value = False

    def activate_solenoid(self, box_number):
        if box_number in self.relays:
            self.relays[box_number].value = True
            time.sleep(5)  # Activation duration
            self.relays[box_number].value = False