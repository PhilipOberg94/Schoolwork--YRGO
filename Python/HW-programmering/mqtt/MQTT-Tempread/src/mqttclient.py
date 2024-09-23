import paho.mqtt.client as mqtt
import glob
import time
import threading

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

    