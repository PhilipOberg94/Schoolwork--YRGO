import time
import board
import busio
import socket
import i2c_lcd
from box_manager import BoxManager

# Pico W TCP settings
PICO_IP = "192.168.4.3"  # Update with Pico W’s IP from minicom
PORT = 8024

class HorseFeeder:
    def __init__(self):
        # I2C setup
        print("Initializing LCD...")
        self.lcd = i2c_lcd.I2CLCD()

        # Box setup
        self.box_manager = [
            BoxManager("Box 1&2"),
            BoxManager("Box 3&4"),
            BoxManager("Box 5&6"),
            BoxManager("Box 7&8")
        ]
        self.box_index = 0
        self.last_lcd_update = ["", ""]

    def switch_box(self, direction):
        if direction == "next":
            self.box_index = (self.box_index + 1) % len(self.box_manager)
        elif direction == "previous":
            self.box_index = (self.box_index - 1) % len(self.box_manager)
        print(f"Switched to box {self.box_index + 1}")

    def send_command(self, command):
        """Send TCP command to Pico W."""
        try:
            print(f"Opening socket to {PICO_IP}:{PORT}...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((PICO_IP, PORT))
            print(f"Sending command: {command}")
            s.send((command + "\r\n").encode())
            response = s.recv(1024).decode().strip()
            print(f"Received: {response}")
            s.close()
            return response
        except Exception as e:
            print(f"TCP Error: {e}")
            return None

    def get_time(self):
        """Use system time until RTC is available."""
        return time.strftime('%H:%M', time.localtime())

    def compare_time(self, current_time, box_time):
        return current_time == box_time

    def run(self):
        print("Entering main loop...")
        try:
            while True:
                current_time = self.get_time()
                print(f"Current time: {current_time}")
                
                # Time-based relay activation
                for box_index, current_box in enumerate(self.box_manager):
                    box_time = current_box.get_boxtime()
                    print(f"Checking box {box_index + 1}: {box_time}")
                    if self.compare_time(current_time, box_time):
                        group = f"Group {box_index + 1}"
                        print(f"Time match for {group}")
                        self.send_command(group)

                # Button handling (LCD shield buttons)
                current_box = self.box_manager[self.box_index]
                if self.lcd.up_button:
                    current_box.increment_boxtime()
                    print("Up button pressed")
                    time.sleep(0.05)
                if self.lcd.down_button:
                    current_box.decrement_boxtime()
                    print("Down button pressed")
                    time.sleep(0.05)
                if self.lcd.left_button:
                    self.switch_box("previous")
                    print("Left button pressed")
                    time.sleep(0.05)
                if self.lcd.right_button:
                    self.switch_box("next")
                    print("Right button pressed")
                    time.sleep(0.05)
                if self.lcd.select_button:
                    print("Select button pressed (no RTC to set)")
                    time.sleep(0.05)

                # Update LCD (16-char limit per line)
                # Line 1: Current time (e.g., "Time: 14:30")
                # Line 2: "Box 1&2 12:00" (when ON) or "Box 1&2 OFF" (when OFF)
                time_message = f"Time: {current_time}"
                if current_box.is_active():
                    box_message = f"{current_box.box_name} {current_box.get_boxtime()}"
                else:
                    box_message = f"{current_box.box_name} OFF"
                # Truncate to fit 16 chars if needed
                box_message = box_message[:16]

                if time_message != self.last_lcd_update[0]:
                    print(f"Updating LCD line 1: {time_message}")
                    self.lcd.display_message(time_message, 1)
                    self.last_lcd_update[0] = time_message
                if box_message != self.last_lcd_update[1]:
                    print(f"Updating LCD line 2: {box_message}")
                    self.lcd.display_message(box_message, 2)
                    self.last_lcd_update[1] = box_message

                time.sleep(0.1)

        except KeyboardInterrupt:
            self.lcd.clear()
            print("Program stopped by user.")

if __name__ == "__main__":
    print("Starting HorseFeeder on Pi Zero...")
    feeder = HorseFeeder()
    feeder.run()
