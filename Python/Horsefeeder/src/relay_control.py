import RPi.GPIO as GPIO
from time_manager import TimeManager

class RelayControl:
    def __init__(self, box_manager):
        self.box_manager = box_manager
        self.relay_pins = {
            1: 17,  # Solenoid control pin for Box 1
        }
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pins[1], GPIO.OUT)
        self.time_manager = TimeManager()

    def activate_solenoid(self, box_number):
        GPIO.output(self.relay_pins[box_number], GPIO.HIGH)
        print(f"Solenoid for Box {box_number} activated")

    def deactivate_solenoid(self, box_number):
        GPIO.output(self.relay_pins[box_number], GPIO.LOW)
        print(f"Solenoid for Box {box_number} deactivated")

    def check_and_open_boxes(self):
        current_time = self.time_manager.get_current_time()
        current_hour, current_minute = current_time.hour, current_time.minute

        for box_number, (hour, minute) in self.box_manager.box_times.items():
            if current_hour == hour and current_minute == minute:
                self.activate_solenoid(box_number)
            else:
                self.deactivate_solenoid(box_number)

    def cleanup(self):
        GPIO.cleanup()
