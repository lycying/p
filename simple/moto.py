import RPi.GPIO as gpio
import time
DELAY = 0.01
gpio.setmode(gpio.BCM)
gpio.setup(22, gpio.OUT)
gpio.setup(21, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(17, gpio.OUT)
while True:
    for step in range(1,5):
        time.sleep(DELAY)
        if step == 1:
            gpio.output(22, gpio.HIGH)
            gpio.output(21, gpio.LOW)
            gpio.output(18, gpio.LOW)
            gpio.output(17, gpio.LOW)
        elif step == 2:
            gpio.output(22, gpio.LOW)
            gpio.output(21, gpio.HIGH)
            gpio.output(18, gpio.LOW)
            gpio.output(17, gpio.LOW)
        elif step == 3:
            gpio.output(22, gpio.LOW)
            gpio.output(21, gpio.LOW)
            gpio.output(18, gpio.HIGH)
            gpio.output(17, gpio.LOW)
        elif step == 4:
            gpio.output(22, gpio.LOW)
            gpio.output(21, gpio.LOW)
            gpio.output(18, gpio.LOW)
            gpio.output(17, gpio.HIGH)
