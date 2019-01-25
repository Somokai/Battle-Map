# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 19:10:41 2019

@author: uberg
"""

from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

vs = VideoStream(src=2).start()
time.sleep(2.0)



# loop over the frames from the video stream

color1Lower = (0,0,92) #Background
color1Upper = (143,71,255) #Background

while True:
    # read the next frame from the video stream and resize it
    frame = vs.read()
    
    
 
    # construct a blob from the frame, pass it through the network,
    # obtain our output predictions, and initialize the list of
    # bounding box rectangles
    #blob = cv2.dnn.blobFromImage(frame, 1.0, (W, H),
     #   (104.0, 177.0, 123.0))
   # net.setInput(blob)
    #detections = net.forward()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask1 = cv2.inRange(hsv, color1Lower, color1Upper)
    mask1 = cv2.bitwise_not(mask1)
    mask1 = cv2.erode(mask1, None, iterations=4)
    mask1 = cv2.dilate(mask1, None, iterations=4)
    cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    for i in range(0,len(cnts)):
        
        ((x,y),radius) = cv2.minEnclosingCircle(cnts[i])
        cv2.circle(frame, (int(x), int(y)), int(radius),
            (0,0,255), 1)
    
    
        # show the output frame
    cv2.imshow("Mask",mask1)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()