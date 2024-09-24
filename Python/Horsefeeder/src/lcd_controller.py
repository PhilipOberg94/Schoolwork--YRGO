import LCD_1in44
from PIL import Image, ImageDraw, ImageFont

class LCDController:
    def __init__(self):
        self.lcd = LCD_1in44.LCD()
        self.init_lcd()

    def init_lcd(self):
        Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  # Default scan direction
        self.lcd.LCD_Init(Lcd_ScanDir)
        self.lcd.LCD_Clear()

    def display_message(self, message):
        self.lcd.LCD_Clear()
        image = Image.new("RGB", (self.lcd.width, self.lcd.height), "WHITE")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
        draw.text((10, 10), message, fill="BLUE", font=font)
        self.lcd.LCD_ShowImage(image, 0, 0)
