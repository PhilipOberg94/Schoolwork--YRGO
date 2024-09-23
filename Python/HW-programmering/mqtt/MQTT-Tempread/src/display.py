import spidev

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