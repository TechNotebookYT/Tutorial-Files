import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

# Green LED
GPIO.setup(20, GPIO.OUT)

# Yellow LED
GPIO.setup(26, GPIO.OUT)

# Red LED
GPIO.setup(21, GPIO.OUT)



try:
    while True:
        GPIO.output(21, GPIO.HIGH)
        print("Red")
        time.sleep(4)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(26, GPIO.HIGH)
        print("Yellow")
        time.sleep(4)
        GPIO.output(26, GPIO.LOW)
        GPIO.output(20, GPIO.HIGH)
        print("Green")
        time.sleep(4)
        print("----------")
        GPIO.output(20, GPIO.LOW)

finally:
    GPIO.cleanup()
