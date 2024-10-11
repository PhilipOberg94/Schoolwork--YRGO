import time

class ledColor:
    blue = '\033[94m' + '█' + '\033[0m'
    green = '\033[92m' + '█' + '\033[0m'
    yellow = '\033[93m' + '█' + '\033[0m'
    red = '\033[91m' + '█' + '\033[0m'
    gray = '\033[90m' + '█' + '\033[0m'

class led:
    def __init__(self, color: ledColor, on: bool):
        self.color = color
        self.on = on

    def turnOn(self):
        self.on = True
    
    def turnOff(self):
        self.on = False
    
    def showLed(self):
        if (self.on == True):
            return self.color
        elif(self.on == False):
            return ledColor.gray
        
class leds:
    def __init__(self, leds: list[led],delay:float):
        self.leds = leds
        self.delay = delay
        self.activeLed = 0
    def startRunningLight(self):
        while (1):
            output = ""
            for d  in self.leds:
                output += str(d.showLed())
            print(output)
            time.sleep(1)
            self.leds[self.activeLed].turnOff()

            if (self.activeLed < len(self.leds)-1):
                self.activeLed+=1
            else:
                self.activeLed = 0