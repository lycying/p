import serial
import RPi.GPIO as GPIO
import time
import signal
import atexit

atexit.register(GPIO.cleanup)  

servopin = 23
servopin2 = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)


GPIO.setup(servopin, GPIO.OUT, initial=False)
GPIO.setup(servopin2, GPIO.OUT, initial=False)

ser = serial.Serial('/dev/ttyAMA0', 18400 , timeout=1)
ser.close()
ser.open()
ser.write("ready\r\n")

while True:
    ser.write("l")
    time.sleep(2)
    ser.write("r")
    time.sleep(2)
    ser.write("u")
    time.sleep(2)
    ser.write("d")
    time.sleep(2)
    print("ok")

