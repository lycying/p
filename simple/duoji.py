#!/usr/bin/env python  
import RPi.GPIO as GPIO
import time
import signal
import atexit

atexit.register(GPIO.cleanup)  

servopin = 23
servopin2 = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
GPIO.setup(servopin2, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin,50)
p2 = GPIO.PWM(servopin2,50)
p.start(0)
p2.start(0)
time.sleep(2)

while(True):
    for i in range(0,181,10):
        p.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.01) 
        print("wa")

    for i in range(181,0,-10):
        p.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.01)
        print(".\c")

    for i in range(0,181,10):
        p2.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.01) 
        print("wa2")

    for i in range(181,0,-10):
        p2.ChangeDutyCycle(2.5 + 10 * i / 180)
        time.sleep(0.01)
        print(".\c2")
