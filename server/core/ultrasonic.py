#!/usr/bin/python
import time
none_pi = False
try:
    import RPi.GPIO as io
except:
    none_pi = True
from threading import Thread

# -----------------------
# Define some functions
# -----------------------
def measure():
  # This function measures a distance

  io.output(io_TRIGGER, True)
  time.sleep(0.00001)
  io.output(io_TRIGGER, False)
  start = time.time()
  
  while io.input(io_ECHO)==0:
    start = time.time()

  while io.input(io_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.

  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

io_TRIGGER = 23
io_ECHO    = 24
class Thread_Ultrasonic(Thread):
    def __init__(self): 
        Thread.__init__(self) 
        if not none_pi:
            io.setmode(io.BCM)
            io.setup(io_TRIGGER,io.OUT)  # Trigger
            io.setup(io_ECHO,io.IN)      # Echo
            io.output(io_TRIGGER, False)
        self.stop = False
        self.distance = 0
    def start(self):
        Thread.start(self)
        print("Ultrasonic mainloop started")

    def run(self):
        while not self.stop:
            time.sleep(1)
            if not none_pi:
                distance = measure_average()
                self.distance = distance

    def close(self):
        self.stop = True

    def getdistance(self):
        return self.distance
