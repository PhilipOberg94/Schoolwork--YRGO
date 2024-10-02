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
            self.lcd.cursor_position(1, 0)
        elif line == 2:
            self.lcd.cursor_position(1, 1)
        self.lcd.message = message

    def clear(self):
        """Clear the LCD display."""
        self.lcd.clear()

    def set_color(self, r, g, b):
        """Set the color of the LCD backlight."""
        self.lcd.color = [r, g, b]  # Set RGB color values
