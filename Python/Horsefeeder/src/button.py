import RPi.GPIO as GPIO

class ButtonManager:
    def __init__(self):
        # Set up GPIO pin numbers for the buttons
        self.button_pins = {
            'up': 17,    # Replace with the GPIO pin for the "up" button
            'down': 27   # Replace with the GPIO pin for the "down" button
        }
        GPIO.setmode(GPIO.BCM)  # Use BCM numbering
        GPIO.setup(self.button_pins['up'], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up "up" button with pull-up
        GPIO.setup(self.button_pins['down'], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up "down" button with pull-up

    def read_button(self):
        if GPIO.input(self.button_pins['up']) == GPIO.LOW:
            return 'up'
        elif GPIO.input(self.button_pins['down']) == GPIO.LOW:
            return 'down'
        else:
            return None
