import RPi.GPIO as GPIO
import time

# Define the GPIO pin connected to the relay's IN pin
RELAY_PIN = 1  # BCM 16 (Physical Pin 36); adjust as needed

def setup():
    # Set GPIO mode to BCM numbering
    GPIO.setmode(GPIO.BCM)
    # Set up the relay pin as an output
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    # Initially set the relay to OFF (HIGH for active-low relays)
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("GPIO setup complete")

def test_relay():
    print("Starting relay test...")
    try:
        while True:
            # Turn relay ON (active-low: LOW = ON)
            GPIO.output(RELAY_PIN, GPIO.LOW)
            print("Relay ON")
            time.sleep(2)  # Wait 2 seconds

            # Turn relay OFF (active-low: HIGH = OFF)
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            print("Relay OFF")
            time.sleep(2)  # Wait 2 seconds

    except KeyboardInterrupt:
        print("Test stopped")
    finally:
        # Cleanup GPIO settings
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Ensure relay is OFF
        GPIO.cleanup()
        print("GPIO cleanup complete")

if __name__ == "__main__":
    setup()
    test_relay()