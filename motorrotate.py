import RPi.GPIO as GPIO
import time

# Define the GPIO pins for your motors
motor_pins = [2, 3, 4, 5, 6, 7, 8]  # Change these to match your setup

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Function to control a single motor
def rotate_motor(motor_num):
    if motor_num in range(1, 8):  # Assuming motor numbers are between 1 and 7
        pin = motor_pins[motor_num - 1]
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)  # Rotate the motor for 1 second (adjust as needed)
        GPIO.output(pin, GPIO.LOW) 