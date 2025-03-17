import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 1  # Test GPIO 16 first
# pin = 2  # Uncomment to test GPIO 2 instead
GPIO.setup(pin, GPIO.OUT)
try:
    GPIO.output(pin, GPIO.LOW)  # ON (active-low)
    print(f"Set GPIO {pin} LOW (ON)")
    time.sleep(2)
    GPIO.output(pin, GPIO.HIGH)  # OFF
    print(f"Set GPIO {pin} HIGH (OFF)")
    time.sleep(2)
except Exception as e:
    print(f"Error: {e}")
finally:
    GPIO.cleanup()