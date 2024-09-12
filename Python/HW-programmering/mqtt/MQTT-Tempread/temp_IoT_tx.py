import spidev # To handle SPI communication
import time
import os
import glob
import paho.mqtt.client as mqtt
import threading  # To handle threads
import RPi.GPIO as GPIO

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

    def stopRunningLight(self):
        self.running = False  # Set the flag to False to stop the running light
        if self.runningLight.is_alive():
            self.runningLight.join()    # Wait for the thread to finish
        for d in self.leds:
            d.turnOff()  # Turn off all LEDs
        print("All LEDs turned off")

# -------------------------------------------------------------
# Temperaturavläsning
# -------------------------------------------------------------
class TempReader:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def read_temp_raw(self): # Read the raw temperature data
        with open(self.device_file, 'r') as f:
            lines = f.readlines()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines and lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        if lines:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return f"{temp_c:.3f}"
        return "Error"

# -------------------------------------------------------------
# Mqtt-client
# -------------------------------------------------------------
class MQTTClient:
    def __init__(self, running_leds, temp_reader):
        self.running = True
        self.base_dir = '/sys/bus/w1/devices/'
        self.running_leds = running_leds
        self.temp_reader = temp_reader
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.desired_temp = None  # Add attribute to store desired temperature
        
        # Declare threads for class instance
        self.publish_thread = threading.Thread(target=self.publish_temperature)
        self.receive_thread = threading.Thread(target=self.listen_for_messages)
        self.compare_thread = threading.Thread(target=self.compare_temperatures)

    def read_temp_raw(self):
        with open(self.device_file, 'r') as f:
                lines = f.readlines()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        if lines:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return f"{temp_c:.3f}"
        return "Error"  

    # The callback for when the client connects to the server
    def on_connect(self, client, userdata, flags, rc):
        # Subscribing in on_connect() means that 
        # if we lose the connection and reconnect then subscriptions
        client.subscribe("ela23/Öberg_sp")
    
    # The callback for when recieving messages
    def on_message(self, client, userdata, msg):
        raw_payload = msg.payload.decode('utf-8')
        self.desired_temp = float(raw_payload)
        print(f"Desired temperature received: {raw_payload}")

    def compare_temperatures(self):
        while self.running:
            if self.desired_temp is not None:
                current_temp = float(self.temp_reader.read_temp()) #Reads current temp and converts to float
                if current_temp < self.desired_temp:    # Compares current temperature with desired temperature
                    self.running_leds.stopRunningLight()
                    print("Temperature is below desired value")
                    time.sleep(0.2)
                    self.running_leds.startRunningLight()
                elif current_temp > self.desired_temp:  # Compares current temperature with desired temperature
                    self.running_leds.stopRunningLight()
                    print("Temperature is above desired value")
                    time.sleep(0.2)
                    self.running_leds.startRunningLight()
            time.sleep(1)

    def publish_temperature(self):
        while self.running:
            temp_str = self.read_temp()  # Read temperature
            self.last_published_temp = temp_str
            print(f"Publishing temperature: {temp_str}")
            result = self.client.publish("ela23/Öberg", temp_str)  # Publish temperature
            result.wait_for_publish()  # Wait for message to be sent
            time.sleep(1)  # Wait 1 second before next publish

    def listen_for_messages(self):
        self.client.loop_forever()  # Block and wait for messages

    def start(self):
        self.publish_thread.start()  # Start the publish thread
        self.receive_thread.start()  # Start the receive thread
        self.compare_thread.start()  # Start the comparison thread

    def shutdown_mqtt(self):
        self.running = False
        self.publish_thread.join()
        self.client.disconnect()
        self.receive_thread.join()
        self.compare_thread.join()
        print("All threads are shut down")
        leds.stopRunningLight()
        GPIO.cleanup()
        self.client.disconnect()
# -------------------------------------------------------------
# MAX7219 Initialization for 7-segment display
# -------------------------------------------------------------
class Display:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Open SPI bus 0, device 0 (CS0)
        self.spi.max_speed_hz = 1200000  # 1.2 MHz

        self.DECODE_MODE = 0x09
        self.INTENSITY = 0x0A
        self.SCAN_LIMIT = 0x0B
        self.SHUTDOWN = 0x0C
        self.DISPLAY_TEST = 0x0F

        self.segment_map = {
            '0': 0b01111110, '1': 0b00110000, '2': 0b01101101, '3': 0b01111001,
            '4': 0b00110011, '5': 0b01011011, '6': 0b01011111, '7': 0b01110000,
            '8': 0b01111111, '9': 0b01111011, ' ': 0b00000000, '.': 0b10000000  # Add decimal point
        }

    def initialize(self):
        self.spi.xfer2([self.DECODE_MODE, 0x00])  # Disable decode mode (raw segment control)
        self.spi.xfer2([self.INTENSITY, 0x08])    # Set intensity (brightness level 0-15)
        self.spi.xfer2([self.SCAN_LIMIT, 0x07])   # Scan all digits (0-7)
        self.spi.xfer2([self.DISPLAY_TEST, 0x00]) # Turn off display test mode
        self.spi.xfer2([self.SHUTDOWN, 0x01])     # Exit shutdown mode (turn on the display)

    def send_digit(self, position, value):
        segment_value = self.segment_map.get(value, 0b00000000)  # Get the segment pattern
        self.spi.xfer2([position, segment_value])  # Send position and segment data

    def display_number(self, number_str):
        position = 8
        i = 0
        while i < len(number_str):
            if number_str[i] == '.':
                self.spi.xfer2([position + 1, self.segment_map[number_str[i - 1]] | self.segment_map['.']])
            else:
                self.send_digit(position, number_str[i])
                position -= 1
            i += 1
            if position < 1:
                break

    def clear_display(self):
        for position in range(1, 9):
            self.spi.xfer2([position, 0b00000000])


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
temp_reader = TempReader()

# Initialize MQTT client
mqtt_client = MQTTClient(running_leds, temp_reader)
mqtt_client.start()

# Initialize display
display = Display()
display.initialize()
display.clear_display()

# Shutdown variable
running = True

try:
    while True:
        temp_str = temp_reader.read_temp()  # Läs temperaturen
        display.display_number(temp_str)  # Visa temperaturen på displayen
        time.sleep(1)  # Uppdatera varje sekund
except KeyboardInterrupt:
    print("Program is shutting down, please wait...")
    mqtt_client.shutdown_mqtt()

