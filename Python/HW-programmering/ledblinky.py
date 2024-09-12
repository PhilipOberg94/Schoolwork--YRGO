import RPi.GPIO as GPIO

# Ställ in GPIO-läget, BCM står för Broadcom SOC channel, detta innebär att man tittar på chippets GPIO-nummer snarare än raspberry pi:s pinnummer
GPIO.setmode(GPIO.BCM)

# Ange GPIO-pinnen som du använder för LED
LED1 = 22
LED2 = 27
LED3 = 17
# Ställ in LED-pinnen som utgång
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

class ledColor:
    blue = 0.03
    green = 0.02
    yellow = 0.02
    red = 0.02

class led:
    def __init__(self, mA:float, on: bool , pin):
        self.mA = mA
        self.on = on
        self.pin = pin

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

    def mAmps(self):
       mA = 0.0
       for i in self.leds:
            mA += i.mA
       return mA

    def startRunningLight(self):
        while (1):
            
            for d in self.leds:
                d.turnOn()
            self.leds[self.activeLed].turnOff()
            time.sleep(self.delay)
            if (self.activeLed < len(self.leds) - 1):
                self.activeLed += 1
            else:
                self.activeLed = 0
            self.leds[self.activeLed].turnOn()

D_pin1 = led(0.03, False, LED1)
D_pin2 = led(0.02, False, LED2)
D_pin3 = led(0.04, False, LED3)

D_list = leds([D_pin1, D_pin2, D_pin3], 1.5)