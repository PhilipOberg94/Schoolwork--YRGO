import paho.mqtt.client as mqtt
import glob
import time
import threading
from led import leds, led
from tempreader import TempReader

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
        self.client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.username_pw_set('oberg94', 'secure1234')
        self.client.connect("a26e229443d3481cb2008a6ffe6c1a97.s1.eu.hivemq.cloud", 8883)
        self.client.subscribe("Öberg_sp", qos=1)
        self.desired_temp = 21  # Set a default desired temperature if no message is received
        print("MQTT client initialized and desired temperature set to 21")
        
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
    def on_connect(self, client, userdata, flags, rc, properties=None):
        # Subscribing in on_connect() means that 
        # if we lose the connection and reconnect then subscriptions
        if rc == 0:
            print("Connected to MQTT broker")
            self.client.subscribe("Öberg_sp")
        else:
            print(f"Connection failed with code {rc}")


    # The callback for when recieving messages
    def on_message(self, client, userdata, msg):
        raw_payload = msg.payload.decode('utf-8')
        self.desired_temp = float(raw_payload)
        print(f"Desired temperature received: {raw_payload}")

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed to topic")

    def desired_temp(self):
        return self.raw_payload

    def compare_temperatures(self):
        while self.running:
            if self.desired_temp is not None:
                # Check if value is a float or error
                try:
                    current_temp = float(self.temp_reader.read_temp()) #Reads current temp and converts to float
                except ValueError:
                    print("Error reading temperature")
                    time.sleep(0.2)
                    continue
                if current_temp < self.desired_temp:    # Compares current temperature with desired temperature
                    self.running_leds.start()
                    time.sleep(0.2)
                elif current_temp > self.desired_temp:  # Compares current temperature with desired temperature
                    self.running_leds.stopRunningLight()
                    time.sleep(0.2)
            time.sleep(1)

    def publish_temperature(self):
        while self.running:
            temp_str = self.read_temp()  # Read temperature
            self.last_published_temp = temp_str
            print(f"Publishing temperature: {temp_str}")
            result = self.client.publish("Öberg_pb", temp_str, qos=1)  # Publish temperature
            result.wait_for_publish()  # Wait for message to be sent
            time.sleep(1)  # Wait 1 second before next publish

    def listen_for_messages(self):
        self.client.loop_forever()  # Block and wait for messages

    def start(self):
        self.publish_thread.start()  # Start the publish thread
        self.receive_thread.start()  # Start the receive thread
        self.compare_thread.start()  # Start the comparison thread

    