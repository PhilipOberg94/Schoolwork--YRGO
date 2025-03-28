import time
import smbus2
import socket
from datetime import datetime
import i2c_lcd
#import relay_control
import time_manager
from box_manager import BoxManager

# TCP configuration
PICO_IP = "192.168.4.3"
PORT = 8024
MAX_RETRIES = 5
RETRY_DELAY = 1.5

class HorseFeeder:
    def __init__(self):
        self.lcd = i2c_lcd.I2CLCD()  # Use the new I2C-based LCD
        self.box_manager = [
            BoxManager("Box 1&2"),  # Maps to Group 1 (Relays 1&2)
            BoxManager("Box 3&4"),  # Maps to Group 2 (Relays 3&4)
            BoxManager("Box 5&6"),  # Maps to Group 3 (Relays 5&6)
            BoxManager("Box 7&8")   # Maps to Group 4 (Relays 7&8)
        ]
        self.time_manager = time_manager.TimeManager()
        self.box_index = 0
        self.last_lcd_update = ["", ""]
        self.sock = None  # TCP socket
        self.connect_to_pico()  # Establish initial connection

    def connect_to_pico(self):
        """Establish a connection to the Pico and update the socket."""
        try:
            if self.sock is not None:
                self.sock.close()  # Close existing socket if any
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            print(f"Attempting to connect to {PICO_IP}:{PORT}")
            with open("./output_file.txt", "a") as file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"Log entry at {current_time}\n")
                file.write(f"Attempting to connect to {PICO_IP}:{PORT}\n")
            self.sock.connect((PICO_IP, PORT))
            print("Connected to Pico")
            with open("./output_file.txt", "a") as file:
                file.write("Connected to Pico\n")
        except ConnectionRefusedError:
            print("Connection refused. Is the Pico server running?")
            with open("./output_file.txt", "a") as file:
                file.write("Connection refused. Is the Pico server running?\n")
            self.sock = None
        except socket.timeout:
            print("Connection timed out. Check IP and network.")
            with open("./output_file.txt", "a") as file:
                file.write("Connection timed out. Check IP and network.\n")
            self.sock = None
        except Exception as e:
            print(f"Error: {e}")
            with open("./output_file.txt", "a") as file:
                file.write(f"Error: {e}\n")
            self.sock = None

    def send_command(self, command):
        """Send a command to the Pico with retries and return the response."""
        if self.sock is None:
            print("No connection available.")
            return None
        
        for attempt in range(MAX_RETRIES):
            with open("./output_file.txt", "a") as file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"Log entry at {current_time}\n")
                try:
                    self.sock.send((command + "\r\n").encode())
                    print(f"Sent command: {command} (Attempt {attempt + 1}/{MAX_RETRIES})")
                    file.write(f"Sent command: {command} (Attempt {attempt + 1}/{MAX_RETRIES})\n")
                    response = self.sock.recv(1024).decode().strip()
                    print("Response:", response)
                    file.write(f"Response: {response}\n")
                    return response
                except socket.timeout:
                    print(f"Connection timed out during communication (Attempt {attempt + 1}/{MAX_RETRIES}).")
                    file.write(f"Connection timed out during communication (Attempt {attempt + 1}/{MAX_RETRIES}).\n")
                    if attempt < MAX_RETRIES - 1:
                        print(f"Retrying in {RETRY_DELAY} second(s)...")
                        time.sleep(RETRY_DELAY)
                    continue
                except Exception as e:
                    print(f"Error: {e} (Attempt {attempt + 1}/{MAX_RETRIES})")
                    file.write(f"Error: {e} (Attempt {attempt + 1}/{MAX_RETRIES})\n")
                    if attempt < MAX_RETRIES - 1:
                        print(f"Retrying in {RETRY_DELAY} second(s)...")
                        time.sleep(RETRY_DELAY)
                    continue
        
        print(f"Failed to get response after {MAX_RETRIES} attempts.")
        with open("./output_file.txt", "a") as file:
            file.write(f"Failed to get response after {MAX_RETRIES} attempts.\n")
        return None

    def activate_relay_group(self, group_num):
        """Send TCP command to activate the specified relay group."""
        command = f"Group {group_num}"
        response = self.send_command(command)
        if response is None:
            print(f"Failed to activate {command}. Attempting to reconnect...")
            self.connect_to_pico()
            if self.sock is not None:
                print("Reconnected successfully. Resending command...")
                response = self.send_command(command)
                if response is None:
                    print(f"Still no response for {command} after reconnection.")
                    return False
        return True

    def switch_box(self, direction):
        if direction == "next":
            self.box_index = (self.box_index + 1) % len(self.box_manager)
        elif direction == "previous":
            self.box_index = (self.box_index - 1) % len(self.box_manager)
        print(f"Switched to box {self.box_index + 1}")

    def run(self):
        try:
            while True:
                current_time = self.time_manager.get_time()

                # Check each box's time slot and activate relays via TCP
                for box_index, current_box in enumerate(self.box_manager):
                    box_time = current_box.get_boxtime()
                    if self.time_manager.compare_time(box_time):  # Fixed: Only pass box_time
                        group_num = box_index + 1  # Box 1&2 -> Group 1, Box 3&4 -> Group 2, etc.
                        self.activate_relay_group(group_num)

                current_box = self.box_manager[self.box_index]

                # Handle button inputs
                if self.lcd.up_button:
                    current_box.increment_boxtime()
                    print("Up button pressed")
                    time.sleep(0.05)

                if self.lcd.down_button:
                    current_box.decrement_boxtime()
                    print("Down button pressed")
                    time.sleep(0.05)

                if self.lcd.left_button:
                    print("Left button pressed")
                    self.switch_box("previous")
                    time.sleep(0.05)

                if self.lcd.right_button:
                    print("Right button pressed")
                    self.switch_box("next")
                    time.sleep(0.05)

                if self.lcd.select_button:
                    self.time_manager.sync_with_system()  # Fixed: Use time_manager, call sync_with_system
                    print("Select button pressed")
                    time.sleep(0.05)

                # Update LCD display
                new_message_box = f"{current_box.box_name}: {current_box.get_boxtime()}"
                if new_message_box != self.last_lcd_update[0]:
                    self.lcd.display_message(new_message_box, 2)
                    self.last_lcd_update[0] = new_message_box
                
                self.lcd.display_message(f"Time: {current_time}", 1)

                time.sleep(0.01)

        except KeyboardInterrupt:
            self.lcd.clear()
            print("Program stopped by user.")
        finally:
            if self.sock is not None:
                self.sock.close()
                print("TCP socket closed.")
                with open("./output_file.txt", "a") as file:
                    file.write("TCP socket closed.\n")

def scan_i2c_bus(bus_number=1):
    bus = smbus2.SMBus(bus_number)
    devices = []
    for address in range(0x03, 0x78):
        try:
            bus.read_byte(address)
            devices.append(hex(address))
        except OSError:
            pass
    bus.close()
    return devices

if __name__ == "__main__":
    print("Scanning I2C bus for devices...")
    devices = scan_i2c_bus()
    if devices:
        print(f"Found I2C devices at addresses: {', '.join(devices)}")
    else:
        print("No I2C devices found.")

    # Initialize and run the HorseFeeder
    feeder = HorseFeeder()
    feeder.run()