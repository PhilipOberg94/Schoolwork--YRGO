import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

class I2CLCD:
    def __init__(self):
        lcd_columns = 16
        lcd_rows = 2

        # Raspberry Pi Pin Setup for the LCD
        self.lcd_rs = digitalio.DigitalInOut(board.D26)
        self.lcd_en = digitalio.DigitalInOut(board.D19)
        self.lcd_d4 = digitalio.DigitalInOut(board.D13)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D5)
        self.lcd_d7 = digitalio.DigitalInOut(board.D11)
        self.lcd_backlight = digitalio.DigitalInOut(board.D4)

        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_en,
            self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
            lcd_columns, lcd_rows, self.lcd_backlight
        )
        self.lcd.backlight = True

    def display_message(self, message):
        self.lcd.clear()
        self.lcd.message = message

    def clear(self):
        self.lcd.clear()
