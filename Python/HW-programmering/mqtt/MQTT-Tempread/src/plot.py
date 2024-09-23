import matplotlib.pyplot as plt
import time
import threading

from mqttclient import MQTTClient

# -------------------------------------------------------------
# Plot the current and desired temperature
# -------------------------------------------------------------
class Plotter:
	def __init__(self):
		self.current_temp = []
		self.desired_temp = []
		self.timestamps = []
		self.running = False

	def add_data(self, current_temp, desired_temp):
		self.current_temp.append(float(current_temp))
		self.desired_temp.append(float(desired_temp))
		self.timestamps.append(time.time())

	def plot_temperature(self): # Plot the current and desired temperature
		plt.ion()  # Enable interactive mode
		fig, ax = plt.subplots()
		while self.running:
			if self.current_temp and self.desired_temp:
				ax.clear()
				ax.plot(self.timestamps, self.current_temp, label='Current Temperature (°C)')
				ax.plot(self.timestamps, self.desired_temp, label='Desired Temperature (°C)')
				ax.set_xlabel('Time')
				ax.set_ylabel('Temperature (°C)')
				ax.legend()
				plt.draw()
				plt.pause(1) 
			time.sleep(1)

	def save_plot(self, filename): # Save the plot to a file
		plt.ioff()  # Disable interactive mode
		fig, ax = plt.subplots()
		ax.plot(self.timestamps, self.current_temp, label='Current Temperature (°C)')
		ax.plot(self.timestamps, self.desired_temp, label='Desired Temperature (°C)')
		ax.set_xlabel('Time')
		ax.set_ylabel('Temperature (°C)')
		ax.legend()
		plt.savefig(filename)
		plt.close(fig)

	def start(self):
		self.running = True
		self.plot_thread = threading.Thread(target=self.plot_temperature)
		self.plot_thread.start()

	def stop(self):
		self.running = False
		self.plot_thread.join()