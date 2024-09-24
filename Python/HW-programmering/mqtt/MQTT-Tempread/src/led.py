import RPi.GPIO as GPIO
import time
import threading

# -------------------------------------------------------------
# Control the LEDs
# -------------------------------------------------------------
class led:
    def __init__(self, on: bool , pin):
        self.on = on
        self.pin = pin
        self.setup_gpio()
        GPIO.setwarnings(False)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        

    def turnOn(self):
        self.on = True
        GPIO.output(self.pin, GPIO.HIGH)

    def turnOff(self):
        self.on = False
        GPIO.output(self.pin, GPIO.LOW)

class leds:
    def __init__(self, leds: list[led], delay: float):
        self.leds = leds
        self.delay = delay
        self.activeLed = 0
        self.running = True
        self.runningLight = threading.Thread(target=self.startRunningLight)

    def startRunningLight(self):
            self.running = True
            while self.running:
                for d in self.leds:
                    d.turnOn()
                self.leds[self.activeLed].turnOff()
                time.sleep(self.delay)
                self.activeLed = (self.activeLed + 1) % len(self.leds)
                self.leds[self.activeLed].turnOn()

    def start(self):
        if not self.runningLight.is_alive():
            self.running = True
            self.runningLight = threading.Thread(target=self.startRunningLight)
            self.runningLight.start()
            print("Running light thread started")

    def stopRunningLight(self):
        self.running = False
        if self.runningLight.is_alive():
            self.runningLight.join()
            print("Running light thread stopped")
        for d in self.leds:
            d.turnOff()


        