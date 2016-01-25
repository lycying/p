import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(22, gpio.OUT)
gpio.setup(21, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(17, gpio.OUT)
while True:
    gpio.output(22, gpio.HIGH)
    gpio.output(17, gpio.HIGH)
    gpio.output(21, gpio.LOW)
    gpio.output(18, gpio.LOW)
