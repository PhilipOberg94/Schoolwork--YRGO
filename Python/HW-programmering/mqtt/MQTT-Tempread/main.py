import sys
import os
import time
import RPi.GPIO as GPIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))  # Add parent directory to path

from src import leds, Display, TempReader, MQTTClient, Plotter
from src import temp_reader, display, mqtt_client, plotter, output_file, running_leds

# Shutdown sequence
def shutdown_seq():
        mqtt_client.running = False
        mqtt_client.publish_thread.join()
        mqtt_client.client.disconnect()
        mqtt_client.receive_thread.join()
        mqtt_client.compare_thread.join()
        plotter.stop()
        plotter.save_plot(output_file)
        print("Plot saved to file")
        running_leds.stopRunningLight()
        print("All threads are shut down")
        print("All LEDs turned off")
        GPIO.cleanup()
        mqtt_client.client.disconnect()

try:
    while True:
        temp_str = temp_reader.read_temp()  # Read temperature
        display.display_number(temp_str)  # Display temperature    
        if mqtt_client.desired_temp is not None:  # Compare temperatures
            plotter.add_data(temp_str, mqtt_client.desired_temp)  # Add temperature to plotter
        else:
            plotter.add_data(temp_str, 25)  # Add temperature to plotter
        time.sleep(0.5)  # Update temperature every 0.5 seconds
except KeyboardInterrupt:
    print("\nProgram is shutting down, please wait...")
    shutdown_seq()

