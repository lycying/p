#!/bin/python
none_pi = False
try:
    import RPi.GPIO as io
except:
    none_pi = True
import time
from threading import Thread

PIR_PIN = 7
class Thread_Motion(Thread):
    def __init__(self): 
        Thread.__init__(self) 
        if not none_pi:
            io.setmode(io.BCM)
            io.setup(PIR_PIN, io.IN)
        self.stop = False
        self.trigger = False

    def istrigger(self):
        return self.trigger

    def start(self):
        Thread.start(self)
        print("Motion mainloop started")
        time.sleep(2)

    def run(self):
        while not self.stop:
            self.trigger = False
            if not none_pi and io.input(PIR_PIN):
                self.trigger = True
            time.sleep(0.3)
    def close(self):
        self.stop = True
