#!/bin/python
"""
The Raspberry Pi Camera Module is a 5 megapixel custom designed add-on for Raspberry Pi, featuring a fixed focus lens. It's capable of 2592 x 1944 pixel static images, and also supports 1080p30, 720p60 and 640x480p60/90 video. It attaches to Pi by way of one of the small sockets on the board upper surface and uses the dedicated CSi interface, designed especially for interfacing to cameras.

*5 megapixel native resolution sensor-capable of 2592 x 1944 pixel static images
*Supports 1080p30, 720p60 and 640x480p60/90 video
*Camera is supported in the latest version of Raspbian, Raspberry Pi's preferred operating system

The board itself is tiny, at around 25mm x 20mm x 9mm. It also weighs just over 3g, making it perfect for mobile or other applications where size and weight are important. It connects to Raspberry Pi by way of a short ribbon cable.

The sensor itself has a native resolution of 5 megapixel, and has a fixed focus lens on-board. In terms of still images, the camera is capable of 2592 x 1944 pixel static images, and also supports 1080p30, 720p60 and 640x480p60/90 video.

The camera is supported in the latest version of Raspbian, Raspberry Pi’s preferred operating system.
"""

nopi = False
try:
    import picamera
except:
    nopi = True
import io
import time
import os 
from threading import Thread

def previewjpeg():
    if nopi: 
        print("no picamera, cannot take photo")
        return False
    with picamera.PiCamera() as camera:
        my_stream = io.BytesIO()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(my_stream,'jpeg')
        camera.stop_preview()
        return my_stream

class Thread_Capture(Thread):
    def __init__(self): 
        Thread.__init__(self) 
        self.stop = False

    def start(self):
        Thread.start(self)
        print("Capture mainloop started")

    def close(self):
        self.stop = True

    def mkdir_p(self,path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def secondwait(self,second):
        for i in range(second):
            time.sleep(1)
            if self.stop:
                break

    def run(self):
        while not self.stop:
            pdir = time.strftime("/srv/http/pics/%Y/%m/%d/")
            pic  = pdir+time.strftime('%Y%m%d%H%M%S.jpg')
            if not nopi:
                if os.path.isdir(pdir): 
                    pass 
                else: 
                    self.mkdir_p(pdir)
                with picamera.PiCamera() as camera:
                    camera.resolution = (512,384)
                    camera.framerate = 30
                    camera.start_preview()
                    self.secondwait(60)
                    camera.capture(pic)
                    camera.stop_preview()
            else:
                self.secondwait(60)
            print("Capture to %s" % pic)

