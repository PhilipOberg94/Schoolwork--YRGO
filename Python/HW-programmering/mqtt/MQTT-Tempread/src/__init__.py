

import RPi.GPIO as GPIO

from .led import led, leds           # Import the LED classes
from .tempreader import TempReader   # Import the TempReader class
from .display import Display         # Import the Display class
from .mqttclient import MQTTClient   # Import the MQTTClient class
from .plot import Plotter            # Import the Plotter class

# -------------------------------------------------------------
# Init file for the MQTT-Tempread project
# -------------------------------------------------------------

# Disable GPIO warnings
GPIO.setwarnings(False)

# Initialize LEDs
LED1 = led(False, 22)
LED2 = led(False, 27)
LED3 = led(False, 17)
leds_list = [LED1, LED2, LED3]
running_leds = leds(leds_list, 0.5)

# Initialize temperature reader
temp_reader = TempReader()

# Initialize plotter
plotter = Plotter()
plotter.start()

# Output file for plot
output_file = "/home/oberg/Schoolwork--YRGO/Python/HW-programmering/mqtt/MQTT-Tempread/output_files/temp_plot.png"

# Initialize MQTT client
mqtt_client = MQTTClient(running_leds, temp_reader)
mqtt_client.start()

# Initialize display
display = Display()
display.initialize()
display.clear_display()

# Shutdown variable
running = True