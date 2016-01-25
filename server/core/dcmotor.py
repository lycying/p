import time

none_pi = False
try:
    import RPi.GPIO as io
except:
    none_pi = True

from threading import Thread
from queue import Queue
# pins attribution
#motor A
in1_pin = 18
in2_pin = 17

#motor B
in3_pin = 27 #21
in4_pin = 22

# always stop motors after xx seconds..
securetime = 10

#misc def
turntime = .04

quitcmd = "_quit_0x00_pi_"

class Thread_DCMotor(Thread):
    cmds = Queue() 
    def __init__(self): 
        Thread.__init__(self) 
        if not none_pi:
            io.setmode(io.BCM)
            io.setup(in1_pin, io.OUT)
            io.setup(in2_pin, io.OUT)
            io.setup(in3_pin, io.OUT)
            io.setup(in4_pin, io.OUT)

    def close(self):
        self.cmds.put(quitcmd)
        if not none_pi:
            io.output(in1_pin, io.LOW)
            io.output(in2_pin, io.LOW)
            io.output(in3_pin, io.LOW)
            io.output(in4_pin, io.LOW)

    #params
    #   dir: left|right
    def turn(self,dir):
        if dir == "right":
            if none_pi:
                print("Dcmotor Turn right")
            else:
                io.output(in1_pin, io.LOW)
                io.output(in2_pin, io.HIGH)
                io.output(in3_pin, io.LOW)
                io.output(in4_pin, io.LOW)
                time.sleep(turntime)
        if dir == "left":
            if none_pi:
                print("Dcmotor Turn left")
            else:
                io.output(in1_pin, io.HIGH)
                io.output(in2_pin, io.LOW)
                io.output(in3_pin, io.LOW)
                io.output(in4_pin, io.LOW)
                time.sleep(turntime)
    #params
    #   dir: forward|backward
    #   long: how long (to check)
    def drive(self , dir):
        if dir == "forward":
            if none_pi:
                print("Dcmotor forward")
            else:
                io.output(in1_pin, io.LOW)
                io.output(in2_pin, io.HIGH)
                io.output(in3_pin, io.LOW)
                io.output(in4_pin, io.HIGH)
        if dir == "backward":
            if none_pi:
                print("Dcmotor back")
            else:
                io.output(in1_pin, io.HIGH)
                io.output(in2_pin, io.LOW)
                io.output(in3_pin, io.HIGH)
                io.output(in4_pin, io.LOW)
    def stop(self):
        if none_pi:
            print("Dcmotor stop")
        else:
            io.output(in1_pin, io.LOW)
            io.output(in2_pin, io.LOW)
            io.output(in3_pin, io.LOW)
            io.output(in4_pin, io.LOW)
    def start(self):
        Thread.start(self)
        print("Dcmotor mainloop started")
    def run(self):
        while True:
            cmd = self.cmds.get()

            if cmd == "left":
                self.turn("left")
            elif cmd == "right":
                self.turn("right")
            elif cmd == "forward":
                self.drive("forward")
            elif cmd == "backward":
                self.drive("backward")
            elif cmd == "stop":
                self.stop()
            elif cmd==quitcmd:
                print("Dcmotor Thread Quit")
                break
            else:
                print("Dcmotor Unknown cmd <%s>" % cmd)

    def runcmd(self,cmd):
        self.cmds.put(cmd)
