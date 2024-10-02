import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

class I2CLCD:
    def __init__(self):
        # Set up the I2C bus and specify the LCD size
        lcd_columns = 16
        lcd_rows = 2
        i2c = board.I2C()  # Use the default I2C bus (SCL, SDA)

        # Initialize the LCD with I2C
        self.lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
        
        # Optionally, set the color of the LCD backlight (RGB values)
        self.lcd.color = [100, 0, 0]  # Red color for the backlight

    def display_message(self, message, line=1):
        """Display a message on the LCD at the given line (1 or 2)."""
        self.lcd.clear()  # Clear the display
        if line == 1:
            self.lcd.cursor_position(0, 0)
        elif line == 2:
            self.lcd.cursor_position(0, 1)
        self.lcd.message = message

    def clear(self):
        """Clear the LCD display."""
        self.lcd.clear()

    def set_color(self, r, g, b):
        """Set the color of the LCD backlight."""
        self.lcd.color = [r, g, b]  # Set RGB color values


# Create an instance of I2CLCD
lcd = I2CLCD()

lcd.clear()
# Set LCD color to red
lcd.set_color(100, 0, 0)
time.sleep(1)
# Print two line message
lcd.display_message("Hello\nCircuitPython")
# Wait 5s
time.sleep(5)
lcd.clear()
# Print two line message right to left
lcd.lcd.text_direction = lcd.lcd.RIGHT_TO_LEFT
lcd.display_message("Hello\nCircuitPython")
# Wait 5s
time.sleep(5)
# Return text direction to left to right
lcd.lcd.text_direction = lcd.lcd.LEFT_TO_RIGHT
# Display cursor
lcd.clear()
lcd.lcd.cursor = True
lcd.display_message("Cursor! ")
# Wait 5s
time.sleep(5)
# Display blinking cursor
lcd.clear()
lcd.lcd.blink = True
lcd.display_message("Blinky Cursor!")
# Wait 5s
time.sleep(5)
lcd.lcd.blink = False
lcd.clear()
# Create message to scroll
scroll_msg = "<-- Scroll"
lcd.display_message(scroll_msg)
# Scroll to the left
for i in range(len(scroll_msg)):
    time.sleep(0.5)
    lcd.lcd.move_left()
lcd.clear()
time.sleep(1)
lcd.display_message("Going to sleep\nCya later!")
time.sleep(5)
# Turn off LCD backlights and clear text
lcd.set_color(0, 0, 0)
lcd.clear()