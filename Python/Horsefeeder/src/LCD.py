import time
from datetime import datetime, timedelta
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Define GPIO to LCD mapping
lcd_rs = digitalio.DigitalInOut(board.D22)  # Register select pin
lcd_en = digitalio.DigitalInOut(board.D27)  # Enable pin (also used for relay)
lcd_d4 = digitalio.DigitalInOut(board.D25)  # Data pin 4
lcd_d5 = digitalio.DigitalInOut(board.D24)  # Data pin 5
lcd_d6 = digitalio.DigitalInOut(board.D23)  # Data pin 6
lcd_d7 = digitalio.DigitalInOut(board.D18)  # Data pin 7

# Relay pin setup
relay_pin = digitalio.DigitalInOut(board.D17)  # Pin 17 for relay control
relay_pin.direction = digitalio.Direction.OUTPUT
relay_pin.value = True  # Make sure the relay is off initially

# Button setup (use GPIO pins for buttons)
button_inc = digitalio.DigitalInOut(board.D6)  # Increment button
button_inc.direction = digitalio.Direction.INPUT
button_inc.pull = digitalio.Pull.UP  # Pull-up resistor

button_dec = digitalio.DigitalInOut(board.D5)  # Decrement button
button_dec.direction = digitalio.Direction.INPUT
button_dec.pull = digitalio.Pull.UP  # Pull-up resistor

# LCD size constants
LCD_COLUMNS = 16
LCD_ROWS = 2

# Initialize the LCD class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, LCD_COLUMNS, LCD_ROWS)

# Initialize boxtime for both Box 1 and Box 2
boxtime = "16:48:01"  # Current time

def lcd_init():
    """Initializes the LCD by clearing the display and setting the cursor to the home position."""
    lcd.clear()
    lcd.home()

def lcd_string(message, line):
    """Displays a message on a specific line of the LCD screen."""
    if line == 1:
        lcd.cursor_position(0, 0)  # Move cursor to the first line
    elif line == 2:
        lcd.cursor_position(0, 1)  # Move cursor to the second line
    lcd.message = message.ljust(LCD_COLUMNS)  # Display the message, padded to fit the screen width

def lcd_cleanup():
    """Clears the LCD display when the program is interrupted or finished."""
    lcd.clear()

def get_system_time():
    """Fetch the current system time."""
    return datetime.now().time()

def activate_relay():
    """Activate the relay to open the boxes."""
    relay_pin.value = False  # Activate relay
    time.sleep(5)  # Keep the relay activated for 5 seconds (or any time required to open the boxes)
    relay_pin.value = True  # Turn off relay after opening

def increment_boxtime():
    """Increment the boxtime by 15 minutes."""
    global boxtime_time
    boxtime_time += timedelta(minutes=15)

def decrement_boxtime():
    """Decrement the boxtime by 15 minutes."""
    global boxtime_time
    boxtime_time -= timedelta(minutes=15)

def check_buttons():
    """Check the status of the increment and decrement buttons."""
    if not button_inc.value:  # Button is pressed (logic is inverted due to pull-up)
        time.sleep(0.2)  # Debounce delay
        if not button_inc.value:  # Ensure button is still pressed
            increment_boxtime()
            while not button_inc.value:  # Wait for button release
                time.sleep(0.1)

    if not button_dec.value:  # Button is pressed (logic is inverted due to pull-up)
        time.sleep(0.2)  # Debounce delay
        if not button_dec.value:  # Ensure button is still pressed
            decrement_boxtime()
            while not button_dec.value:  # Wait for button release
                time.sleep(0.1)

# Main program logic
try:
    lcd_init()
    while True:

        check_buttons()

        # Get the current system time
        current_time = get_system_time()
        boxtime_time = datetime.strptime(boxtime, '%H:%M:%S').time()

        # Activate the relay if the current time matches the boxtime
        if current_time.strftime('%H:%M:%S') == boxtime_time.strftime('%H:%M:%S'):

            activate_relay()

        # Display the current time and next boxtime on the LCD
        lcd_string(f"Time:  {current_time.strftime('%H:%M')}", 1)
        lcd_string(f"Box 1&2: {boxtime_time.strftime('%H:%M')}" , 2)

        time.sleep(1)

except KeyboardInterrupt:
    lcd_cleanup()
