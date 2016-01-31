import serial
import RPi.GPIO as GPIO
import time
import signal
import atexit

atexit.register(GPIO.cleanup)  

servopin = 23
servopin2 = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
GPIO.setup(servopin2, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin,50)
p2 = GPIO.PWM(servopin2,50)
p.start(0)
p2.start(0)
p.ChangeDutyCycle(0)
p2.ChangeDutyCycle(0)

ser = serial.Serial('/dev/ttyAMA0', 9600 , timeout=1)
ser.close()
ser.open()
ser.write("ready\r\n")


p2_ar = 0
p_ar = 0

try:
    while 1:
        resp = ser.readline().replace("\r\n","")
        if resp == "a1":
            p2_ar = p2_ar + 10
            if p2_ar < 181:
                ser.write("turn to left\r\n")
                p2.ChangeDutyCycle(2.5 + 10 * p2_ar / 180)
                time.sleep(0.1) 
                p2.ChangeDutyCycle(0)
            else:
                p2_ar = p2_ar - 10
                ser.write("left out of range \r\n")

        elif resp == "a2":
            p2_ar = p2_ar - 10
            if p2_ar > -1:
                ser.write("turn to right\r\n")
                p2.ChangeDutyCycle(2.5 + 10 * p2_ar/ 180)
                time.sleep(0.1) 
                p2.ChangeDutyCycle(0)
            else:
                p2_ar = p2_ar + 10
                ser.write("right out of range\r\n")

        elif resp == "b1":
            p_ar = p_ar + 10
            if p_ar < 181:
                ser.write("turn to up\r\n")
                p.ChangeDutyCycle(2.5 + 10 * p_ar / 180)
                time.sleep(0.1) 
                p.ChangeDutyCycle(0)
            else:
                p_ar = p_ar - 10
                ser.write("up out of range \r\n")
        elif resp == "b2":
            p_ar = p_ar - 10
            if p_ar > -1:
                ser.write("turn to down\r\n")
                p.ChangeDutyCycle(2.5 + 10 * p_ar/ 180)
                time.sleep(0.1) 
                p.ChangeDutyCycle(0)
            else:
                p_ar = p_ar + 10
                ser.write("down out of range\r\n")

except KeyboardInterrupt:
    ser.close()
