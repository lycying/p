#!/usr/bin/env python
# coding:utf-8
import sys
import time
from threading import Thread
from threading import Condition

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor

from core.ultrasonic import Thread_Ultrasonic
from core.dcmotor import Thread_DCMotor
from core.motion import Thread_Motion
from core.camera import Thread_Capture
from core.camera import previewjpeg
from core.tts import netTalk

td_dcmotor = Thread_DCMotor()
td_motion  = Thread_Motion()
td_capture = Thread_Capture()
td_ultrasonic = Thread_Ultrasonic()


class Thread_Auto(Thread):
    def __init__(self): 
        Thread.__init__(self) 
        self.stop = False
        self.automode = False
        self.savedistance = 0
    def start(self):
        Thread.start(self)
        print("Auto Mode start...")
    def run(self):
        while not self.stop:
            time.sleep(0.1)
            if self.automode:
                motion_trigger = td_motion.istrigger()
                ultrasonic_distance = td_ultrasonic.getdistance()
                if not ultrasonic_distance == self.savedistance:
                    self.savedistance = ultrasonic_distance
                    print ("Distance : %.1f" % ultrasonic_distance)
                if motion_trigger:
                    print("Motion Deteted!")
    def close(self):
        self.stop = True

td_auto = Thread_Auto()

class CmdProtocol(LineReceiver):
    delimiter = b'\r\n'
    def connectionMade(self):
        self.client_ip = self.transport.getPeer()
        log.msg("Client connection from %s" % self.client_ip)
        if len(self.factory.clients) >= self.factory.clients_max:
            log.msg("Too many connections. bye !")
            self.client_ip = None
            self.transport.loseConnection()
        else:
            self.factory.clients.append(self.client_ip)

    def connectionLost(self, reason):
        log.msg('Lost client connection.  Reason: %s' % reason)
        if self.client_ip:
            self.factory.clients.remove(self.client_ip)

    def lineReceived(self, line):
        line = line.decode("utf-8")
        log.msg('Cmd received from %s : %s' % (self.client_ip, line))
        self.cmdparse(line)

    def cmdparse(self,cmd):
        try:
            if cmd == "exit":
                self.transport.loseConnection()
                return
            elif cmd == "jpeg":
                url = previewjpeg()
                if url:
                    self.transport.write(url)
                else:
                    self.transport.write("nothing")
                    print("nothing to take jpeg")
                return
            elif cmd == "auto":
                td_auto.automode = True
                print("Enter the auto mode , The car will drive itself")
                return
            elif cmd == "manul":
                td_auto.automode = False
                print("Enter the manul mode ,You can control it remote")
                return

            part,partcmd = cmd.split(" ",1)
            if part=="motor":
                td_dcmotor.runcmd(partcmd)
            elif part=="tts":
                reactor.callInThread(netTalk,partcmd)
        except Exception as e:
            print("ahahah...",e)
    
class MyFactory(ServerFactory):
    protocol = CmdProtocol
    def __init__(self, clients_max=10):
        self.clients_max = clients_max
        self.clients = []
def cleanup():
    td_dcmotor.close()
    td_capture.close()
    td_motion.close()
    td_ultrasonic.close()
    td_auto.close()
    log.msg("clean up")
    try:
        import RPi.GPIO as io
        io.cleanup()
    except:
        pass

if __name__ == "__main__":
    reactor.addSystemEventTrigger('before', 'shutdown', cleanup)
    log.startLogging(sys.stdout)
    log.startLogging(open("/tmp/pi.log",'a'))
    td_dcmotor.start()
    td_capture.start()
    td_motion.start()
    td_ultrasonic.start()
    td_auto.start()
    reactor.listenTCP(14000, MyFactory(2))
    reactor.run()
