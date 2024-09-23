import os
import glob
import time

# -------------------------------------------------------------
# Temperature reader
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

    def read_temp(self): # Convert the raw temperature data to a float-value
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