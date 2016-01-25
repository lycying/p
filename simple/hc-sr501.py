#!/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)
try:
    print("Ready !")
    time.sleep(2)
    while True:
        if GPIO.input(PIR_PIN):
            print ("Motion Detected!");
        time.sleep(0.3)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
