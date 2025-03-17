import board

i2c = board.I2C()
print(i2c.scan())  # Add to i2c_lcd.py __init__