import array, time
from machine import Pin, PWM
import rp2
import network
import usocket

ssid = 'Hotspot'
password = 'secure123'
STATIC_IP = "192.168.4.3"
SUBNET = "255.255.255.0"
GATEWAY = "192.168.4.1"
DNS = "192.168.4.1"

# Pico as a TCP server
HOST = STATIC_IP  # Use the variable, not a string literal
PORT = 8024
TCP = 1

NUM_LEDS = 1
PIN_NUM = 13
POWER = 5000

# Initialize PWM
pwm = PWM(Pin(6))
pwm.freq(POWER)

# WS2812 and NeoPixel setup (unchanged)
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1).side(0)    [T3 - 1]
    jmp(not_x, "do_zero").side(1)    [T1 - 1]
    jmp("bitloop").side(1)    [T2 - 1]
    label("do_zero")
    nop().side(0)    [T2 - 1]
    wrap()

class NeoPixel(object):
    def __init__(self, pin=PIN_NUM, num=NUM_LEDS, brightness=0.2):
        self.pin = pin
        self.num = num
        self.brightness = brightness
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
        self.sm.active(1)
        self.ar = array.array("I", [0 for _ in range(self.num)])
        self.ch1 = Pin(21, Pin.OUT)  # Relay 1
        self.ch2 = Pin(20, Pin.OUT)  # Relay 2
        self.ch3 = Pin(19, Pin.OUT)  # Relay 3
        self.ch4 = Pin(18, Pin.OUT)  # Relay 4
        self.ch5 = Pin(17, Pin.OUT)  # Relay 5
        self.ch6 = Pin(16, Pin.OUT)  # Relay 6
        self.ch7 = Pin(15, Pin.OUT)  # Relay 7
        self.ch8 = Pin(14, Pin.OUT)  # Relay 8
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 150, 0)
        self.GREEN = (0, 255, 0)
        self.CYAN = (0, 255, 255)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (180, 0, 255)
        self.WHITE = (255, 255, 255)
        self.groups = {
            'Group 1': [self.ch1, self.ch2],
            'Group 2': [self.ch3, self.ch4],
            'Group 3': [self.ch5, self.ch6],
            'Group 4': [self.ch7, self.ch8]
        }

    def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.num)])
        for i, c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g << 16) + (r << 8) + b
        self.sm.put(dimmer_ar, 8)

    def pixels_set(self, i, color):
        self.ar[i] = (color[1] << 16) + (color[0] << 8) + color[2]

    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.pixels_set(i, color)

    def RGB_OUT(self):
        self.pixels_fill(self.GREEN)
        self.pixels_show()
        time.sleep(0.05)
        self.pixels_fill(self.BLACK)
        self.pixels_show()

    def Relay_CHx(self, pin, switch):
        if switch:
            pin.high()
        else:
            pin.low()

    def relay_pulse(self, pin):
        self.Relay_CHx(pin, True)
        pwm.duty_u16(POWER)
        time.sleep(1)
        pwm.duty_u16(0)
        self.Relay_CHx(pin, False)
        self.RGB_OUT()

    def group_pulse(self, group_name):
        if group_name in self.groups:
            for pin in self.groups[group_name]:
                self.relay_pulse(pin)

if __name__ == '__main__':
    strip = NeoPixel()
    conn = None
    sock = None
    wlan = network.WLAN(network.STA_IF) if TCP == 1 else None

    try:
        if TCP == 1:
            wlan.active(True)
            wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, DNS))
            print("Setting static IP-Address", wlan.ifconfig())
            print("Checking WiFi connection to:", ssid)
            if wlan.isconnected():
                print("Already connected, resetting connection...")
                wlan.disconnect()
                time.sleep(1)
            else:
                print("Not connected yet")

            print("Attempting to connect...")
            wlan.connect(ssid, password)
            timeout = 10
            while not wlan.isconnected() and timeout > 0:
                print("Searching for WiFi... Status:", wlan.status())
                time.sleep(1)
                strip.pixels_fill(strip.YELLOW)
                strip.pixels_show()
                time.sleep(0.1)
                strip.pixels_fill(strip.BLACK)
                strip.pixels_show()
                timeout -= 1

            if wlan.isconnected():
                print('Connected to WiFi')
                status = wlan.ifconfig()
                print('IP = ' + status[0])
            else:
                raise RuntimeError("Failed to connect to WiFi within timeout")

            for attempt in range(3):
                try:
                    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
                    sock.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
                    sock.bind((HOST, PORT))
                    break
                except OSError as e:
                    if e.args[0] == 98:
                        print("Port 8024 in use, waiting 2 seconds, attempt", attempt + 1)
                        time.sleep(2)
                        if attempt == 2:
                            raise
                    else:
                        raise
            sock.listen(1)
            print("Pico listening on", status[0], ":", PORT)
            conn, addr = sock.accept()
            print("Connected by", addr)
            conn.send("Hello, Python client!\r\n".encode())

        while True:
            if TCP == 1:
                try:
                    response = conn.recv(1024).decode().strip()
                    print("Received:", response)
                    if not response:
                        print("Client disconnected, waiting for new connection...")
                        conn.close()
                        conn, addr = sock.accept()
                        print("New connection from", addr)
                        conn.send("Hello, Python client!\r\n".encode())
                        continue
                except Exception as e:
                    print("Receive error:", e)
                    break

                if response == 'Relay 1':
                    strip.relay_pulse(strip.ch1)
                    conn.send("****Relay 1 Pulsed****\n\n".encode())
                elif response == 'Relay 2':
                    strip.relay_pulse(strip.ch2)
                    conn.send("****Relay 2 Pulsed****\n\n".encode())
                elif response == 'Relay 3':
                    strip.relay_pulse(strip.ch3)
                    conn.send("****Relay 3 Pulsed****\n\n".encode())
                elif response == 'Relay 4':
                    strip.relay_pulse(strip.ch4)
                    conn.send("****Relay 4 Pulsed****\n\n".encode())
                elif response == 'Relay 5':
                    strip.relay_pulse(strip.ch5)
                    conn.send("****Relay 5 Pulsed****\n\n".encode())
                elif response == 'Relay 6':
                    strip.relay_pulse(strip.ch6)
                    conn.send("****Relay 6 Pulsed****\n\n".encode())
                elif response == 'Relay 7':
                    strip.relay_pulse(strip.ch7)
                    conn.send("****Relay 7 Pulsed****\n\n".encode())
                elif response == 'Relay 8':
                    strip.relay_pulse(strip.ch8)
                    conn.send("****Relay 8 Pulsed****\n\n".encode())
                elif response == 'Group 1':
                    strip.group_pulse('Group 1')
                    conn.send("****Group 1 Pulsed****\n\n".encode())
                elif response == 'Group 2':
                    strip.group_pulse('Group 2')
                    conn.send("****Group 2 Pulsed****\n\n".encode())
                elif response == 'Group 3':
                    strip.group_pulse('Group 3')
                    conn.send("****Group 3 Pulsed****\n\n".encode())
                elif response == 'Group 4':
                    strip.group_pulse('Group 4')
                    conn.send("****Group 4 Pulsed****\n\n".encode())
                elif response == 'Relay ALL':
                    for i in range(8):
                        strip.Relay_CHx(getattr(strip, f'ch{i+1}'), True)
                    pwm.duty_u16(POWER)
                    time.sleep(1)
                    pwm.duty_u16(0)
                    for i in range(8):
                        strip.Relay_CHx(getattr(strip, f'ch{i+1}'), False)
                    strip.RGB_OUT()
                    conn.send("****Relay ALL Pulsed****\n\n".encode())

            else:
                response = input()

    except KeyboardInterrupt:
        print("KeyboardInterrupt, cleaning up...")
    except Exception as e:
        print("Error:", e)
    finally:
        if conn is not None:
            conn.close()
        if sock is not None:
            sock.close()
        if TCP == 1 and wlan is not None:
            wlan.disconnect()
