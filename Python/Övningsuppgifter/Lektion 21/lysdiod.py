from ledColor import *
        
D_blue = led(ledColor.blue, False)
D_red = led(ledColor.red, False)
D_yellow = led(ledColor.yellow, False)
D_green = led(ledColor.green, False)

ledLista = leds([D_blue, D_red, D_green, D_yellow], 0.5)
ledLista.startRunningLight()

# while(1):
#     print(D_blue.showLed())
#     time.sleep(1)
#     D_blue.turnOn()
#     print(D_blue.showLed())
#     time.sleep(1)
#     D_blue.turnOff()