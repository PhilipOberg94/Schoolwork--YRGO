import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

class I2CLCD:
    def __init__(self):
        # Set up the I2C bus and specify the LCD size
        lcd_columns = 16
        lcd_rows = 2
        i2c = board.I2C()  # Pi Zero’s default I2C (GPIO 2 SDA, GPIO 3 SCL)

        # Initialize the LCD with I2C (MCP23017 default address is 0x20)
        try:
            self.lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows, address=0x20)
            self.lcd.backlight = True
            self.lcd.color = [100, 0, 0]  # Red backlight
            print("LCD initialized successfully")
        except Exception as e:
            print(f"Failed to initialize LCD: {e}")
            self.lcd = None

    def display_message(self, message, line=1):
        """Display a message on the LCD at the given line (1 or 2)."""
        if self.lcd is None:
            print(f"Cannot display '{message}' on line {line}: LCD not initialized")
            return
        try:
            if line == 1:
                self.lcd.cursor_position(0, 0)
            elif line == 2:
                self.lcd.cursor_position(0, 1)
            self.lcd.message = " " * 16  # Clear line
            self.lcd.cursor_position(0, line - 1)
            self.lcd.message = message[:16]  # Truncate to 16 chars
        except Exception as e:
            print(f"Error displaying message '{message}' on line {line}: {e}")

    def clear(self):
        """Clear the LCD display."""
        if self.lcd:
            try:
                self.lcd.clear()
            except Exception as e:
                print(f"Error clearing LCD: {e}")

    def set_color(self, r, g, b):
        """Set RGB backlight color."""
        if self.lcd:
            try:
                self.lcd.color = [r, g, b]
            except Exception as e:
                print(f"Error setting color: {e}")

    # Button properties (supported by Character_LCD_RGB_I2C)
    @property
    def up_button(self):
        return self.lcd.up_button if self.lcd and hasattr(self.lcd, 'up_button') else False

    @property
    def down_button(self):
        return self.lcd.down_button if self.lcd and hasattr(self.lcd, 'down_button') else False

    @property
    def left_button(self):
        return self.lcd.left_button if self.lcd and hasattr(self.lcd, 'left_button') else False

    @property
    def right_button(self):
        return self.lcd.right_button if self.lcd and hasattr(self.lcd, 'right_button') else False

    @property
    def select_button(self):
        return self.lcd.select_button if self.lcd and hasattr(self.lcd, 'select_button') else False