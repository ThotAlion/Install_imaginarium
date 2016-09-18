from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from threading import Thread

class vision(Thread):
        
    def __init__(self):
        # before launching the task
        Thread.__init__(self)
        self.go_on = True
        # declare the camera
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.anglemoy = 0
        # allow the camera to warmup
        time.sleep(0.1)
        
    def run(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array
         
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret2,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
            kernel = np.ones((5,5),np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            
            edges = cv2.Canny(opening,50,150,apertureSize = 3)
            minLineLength = 10
            maxLineGap = 10
            lines = cv2.HoughLines(edges,3,np.pi/180,200)
            sumangle = 0
            nline = 0
            if not(lines is None):
                for rho,theta in lines[0]:
                    sumangle = sumangle + theta
                    nline = nline + 1
                    #print theta.size
                    # a = np.cos(theta)
                    # b = np.sin(theta)
                    # x0 = a*rho
                    # y0 = b*rho
                    # x1 = int(x0 + 1000*(-b))
                    # y1 = int(y0 + 1000*(a))
                    # x2 = int(x0 - 1000*(-b))
                    # y2 = int(y0 - 1000*(a))
                self.anglemoy = (sumangle/nline)*180/np.pi
                print self.anglemoy
            time.sleep(0.1)
            self.rawCapture.truncate(0)
            if self.go_on == False:
                break
            
    def stop(self):
        self.go_on = False
        