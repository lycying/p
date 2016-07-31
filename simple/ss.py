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

DELAY = 0.01

rememberFile = "/home/pi/.steprem"
STEP_VALUE = 0
try:
    STEP_FILE = open(rememberFile,"r")
    STEP_VALUE = int(STEP_FILE.readline())
    STEP_FILE.close()
except:
    open(rememberFile,"w").close()
    STEP_FILE = open(rememberFile,"r+")
    STEP_FILE.write(str(STEP_VALUE))
    STEP_FILE.close()


def writeValue(left):
    global STEP_VALUE
    if left:
        if STEP_VALUE >= 100:
            ser.write("left out of range\r\n")
            return False
        v = 10
    else:
        if STEP_VALUE <= 0:
            ser.write("right out of range\r\n")
            return False
        v = -10
    STEP_FILE = open(rememberFile,"w+")
    STEP_VALUE = STEP_VALUE + v
    STEP_FILE.write(str(STEP_VALUE))
    STEP_FILE.close()
    return True

def turn_left():
    if not writeValue(True):
        return 
    for i in range(30):
        for step in range(1,5):
            time.sleep(DELAY)
            if step == 1:
                GPIO.output(10, GPIO.HIGH)
                GPIO.output(9, GPIO.LOW)
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.LOW)
            elif step == 2:
                GPIO.output(10, GPIO.LOW)
                GPIO.output(9, GPIO.HIGH)
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.LOW)
            elif step == 3:
                GPIO.output(10, GPIO.LOW)
                GPIO.output(9, GPIO.LOW)
                GPIO.output(8, GPIO.HIGH)
                GPIO.output(7, GPIO.LOW)
            elif step == 4:
                GPIO.output(10, GPIO.LOW)
                GPIO.output(9, GPIO.LOW)
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.HIGH)
    ser.write("turn to left:"+str(STEP_VALUE)+"\r\n")

def turn_right():
    if not writeValue(False):
        return
    for i in range(30):
        for step in range(1,5):
            time.sleep(DELAY)
            if step == 1:
                GPIO.output(10, GPIO.LOW)
                GPIO.output(9, GPIO.LOW)
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.HIGH)
            elif step == 2:
                GPIO.output(10, GPIO.LOW)
                GPIO.output(9, GPIO.LOW)
                GPIO.output(8, GPIO.HIGH)
                GPIO.output(7, GPIO.LOW)
            elif step == 3:
                GPIO.output(10, GPIO.LOW)
                GPIO.output(9, GPIO.HIGH)
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.LOW)
            elif step == 4:
                GPIO.output(10, GPIO.HIGH)
                GPIO.output(9, GPIO.LOW)
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.LOW)
    ser.write("turn to right:"+str(STEP_VALUE)+"\r\n")

try:
    while 1:
        resp = ser.readline().replace("\r\n","")
        if resp == "a1":
            turn_left()

        elif resp == "a2":
            turn_right()

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
