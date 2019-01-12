# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import win32api, win32con
import time

def find_and_outline(c, color):
        
    ((x, y), radius) = cv2.minEnclosingCircle(c)

    # only proceed if the radius meets a minimum size
    if radius > 5:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(x), int(y)), int(radius),
            color, 2)
        #cv2.circle(frame, center1, 5, (50, 50, 255), -1)
        #M = cv2.moments(c)
        #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
color1Lower = (58, 57, 43) #green
color1Upper = (179, 255, 255) #green 
# if a video path was not supplied, grab the reference
# to the webcam
camera = cv2.VideoCapture(2)


# keep looping



# construct a mask for the color "green", then perform
# a series of dilations and erosions to remove any small
# blobs left in the mask


    # find contours in the mask and initialize the current
# (x, y) center of the ball


while True:
# only proceed if at least one contour was found

    (grabbed, frame) = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    mask1 = cv2.inRange(hsv, color1Lower, color1Upper)
    mask1 = cv2.erode(mask1, None, iterations=4)
    mask1 = cv2.dilate(mask1, None, iterations=4)
    
    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if len(cnts1) > 0:
        #cnts = [];
        #for i in range(0,3):
        #    cnts.append(max(cnts1,key=cv2.contourArea))
            
        
        for i in range(0,len(cnts1)):
            find_and_outline(cnts1[i],(255,0,0))
            

    cv2.imshow("Frame", frame)        
cv2.waitKey(0) 
cv2.destroyAllWindows() 
    # loop over the set of tracked points
# show the frame to our screen

#key = cv2.waitKey(1) & 0xFF

