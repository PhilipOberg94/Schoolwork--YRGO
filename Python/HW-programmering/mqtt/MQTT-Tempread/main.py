from src.led import led, leds           # Import the LED classes
from src.tempreader import TempReader   # Import the TempReader class
from src.display import Display         # Import the Display class
from src.mqttclient import MQTTClient   # Import the MQTTClient class
import RPi.GPIO as GPIO                 # Import the GPIO library
import time                             # Import the time library
import os                               # Import the os library
import sys                              # Import the sys library
import threading                        # Import the threading library
import paho.mqtt.client as mqtt         # Import the MQTT library
import glob                             # Import the glob library
import spidev                           # Import the spidev library

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))  # Add parent directory to path

# Disable GPIO warnings
GPIO.setwarnings(False)

def shutdown_seq(self):
        mqtt_client.running = False
        mqtt_client.publish_thread.join()
        mqtt_client.client.disconnect()
        mqtt_client.receive_thread.join()
        mqtt_client.compare_thread.join()
        print("All threads are shut down")
        leds.stopRunningLight()
        GPIO.cleanup()
        mqtt_client.client.disconnect()

# -------------------------------------------------------------
# Main logic for the program
# -------------------------------------------------------------
# Initialize LEDs
LED1 = led(False, 22)
LED2 = led(False, 27)
LED3 = led(False, 17)
leds_list = [LED1, LED2, LED3]
running_leds = leds(leds_list, 0.5)

# Initialize temperature reader
try:
    temp_reader = TempReader()
except:
    print("Error: Could not initialize temperature reader")
    exit(1)

# Initialize MQTT client
try:
    mqtt_client = MQTTClient(running_leds, temp_reader)
    mqtt_client.start()
except:
    print("Error: Could not initialize MQTT client")
    exit(1)

# Initialize display
display = Display()
display.initialize()
display.clear_display()

# Shutdown variable
running = True

try:
    while True:
        temp_str = temp_reader.read_temp()  # Läs temperaturen
        print(f"Current temperature: {temp_str}°C")
        #display.display_number(temp_str)  # Visa temperaturen på displayen
        time.sleep(1)  # Uppdatera varje sekund
except KeyboardInterrupt:
    print("Program is shutting down, please wait...")
    shutdown_seq()

