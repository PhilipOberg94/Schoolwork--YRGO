import paho.mqtt.client as mqtt        

# The callback for when the client connects to the server
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that
    # reconnect will renew then subscriptions
    client.subscribe("ela23/Öberg")

# The callback for receiving message
def on_message(client, userdata, msg):
    print(f"{msg.payload}")

# Create a MQTT client with callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Blocking call that processes network traffic, dispatches 
# callbacks and handles reconnecting.
client.loop_forever()