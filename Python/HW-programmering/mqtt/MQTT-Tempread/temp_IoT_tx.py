import spidev
import time
import os
import glob
import paho.mqtt.client as mqtt
import threading  # För att hantera trådning
import RPi.GPIO as GPIO

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
        self.setup_gpio()

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
        self.running = False
        self.runningLight = threading.Thread(target=self.startRunningLight)


    def mAmps(self):
       mA = 0.0
       for i in self.leds:
            mA += i.mA
       return mA

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
            self.runningLight.join()
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

    def read_temp_raw(self):
        try:
            with open(self.device_file, 'r') as f:
                lines = f.readlines()
            return lines
        except FileNotFoundError:
            print("Temperature sensor file not found.")
            return []

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
    def __init__(self, running_leds, temp_reader, base_dir='/sys/bus/w1/devices/', broker_address="test.mosquitto.org", port=1883, keepalive=60):
        self.base_dir = base_dir
        self.running_leds = running_leds
        self.temp_reader = temp_reader
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, port, keepalive)
        self.desired_temp = None  # Add attribute to store desired temperature

    def read_temp_raw(self):
        try:
            with open(self.device_file, 'r') as f:
                lines = f.readlines()
            return lines
        except FileNotFoundError:
            print("Temperature sensor file not found.")
            return []

    def read_temp(self):
        lines = self.read_temp_raw()
        if lines:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return f"{temp_c:.3f}"
        return "Error"  

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("ela23/Öberg_sp")

    def on_message(self, client, userdata, msg):
        compare_payload = msg.payload.decode('utf-8')
        print(f"Desired temperature received: {compare_payload}")
        
        try:
            self.desired_temp = float(compare_payload)
        except ValueError:
            print("Error converting desired temperature to float")
            return

    def compare_temperatures(self):
        while True:
            if self.desired_temp is not None:
                current_temp = self.temp_reader.read_temp()
                print(f"Current temperature: {current_temp}")
                
                try:
                    current_temp_float = float(current_temp)
                except ValueError:
                    print("Error converting current temperature to float")
                    continue
                
                print(f"Comparing current temperature ({current_temp_float}) with desired temperature ({self.desired_temp})")
                if current_temp_float <= self.desired_temp:
                    print("Turning on the heater")
                    if not self.running_leds.runningLight.is_alive():
                        self.running_leds.runningLight = threading.Thread(target=self.running_leds.startRunningLight)
                        self.running_leds.runningLight.start()
                else:
                    print("Turning off the heater")
                    if self.running_leds.runningLight.is_alive():
                        self.running_leds.stopRunningLight()
            time.sleep(1)  # Check every second

    def publish_temperature(self):
        while True:
            temp_str = self.read_temp()  # Read temperature
            self.last_published_temp = temp_str
            print(f"Publishing temperature: {temp_str}")
            result = self.client.publish("ela23/Öberg", temp_str)  # Publish temperature
            result.wait_for_publish()  # Wait for message to be sent
            time.sleep(1)  # Wait 1 second before next publish

    def listen_for_messages(self):
        self.client.loop_forever()  # Block and wait for messages

    def start(self):
        publish_thread = threading.Thread(target=self.publish_temperature)
        receive_thread = threading.Thread(target=self.listen_for_messages)
        compare_thread = threading.Thread(target=self.compare_temperatures)  # Start comparison thread

        publish_thread.start()
        receive_thread.start()
        compare_thread.start()  # Start the comparison thread
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
        length = len(number_str.replace('.', ''))  # Count of digits without decimal points
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
LED1 = led(20.0, False, 22)
LED2 = led(20.0, False, 27)
LED3 = led(20.0, False, 17)
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

try:
    while True:
        temp_str = temp_reader.read_temp()  # Läs temperaturen
        display.display_number(temp_str)  # Visa temperaturen på displayen
        time.sleep(1)  # Uppdatera varje sekund
except KeyboardInterrupt:
    pass
finally:
    display.clear_display()
    display.spi.close()  # Stäng SPI-gränssnittet när programmet avslutas
    running_leds.stopRunningLight()
    GPIO.cleanup()
