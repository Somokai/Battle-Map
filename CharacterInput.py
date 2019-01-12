# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 09:57:31 2019

@author: uberg
"""
# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import win32api, win32con
import time
 

    
def find_and_outline(c, color,printed,playerCharacters):
        
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        encircled = 0;
		# only proceed if the radius meets a minimum size
        if radius > 5 and radius < 100:
            #print(c.shape)
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                color, 1)
            #M = cv2.moments(c)
            #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            encircled = encircled+1
            #cv2.circle(frame, center1, 5, (50, 50, 255), -1)
            if printed == 0:
                name = str(input('Who is this? '))
                return (encircled, ((x,y),radius), name)
            if printed == 1:
                prevDist = 1e6
                for key in playerCharacters:
                    a = playerCharacters[key][0]
                    b = np.array((x,y))
                    dist = np.linalg.norm(a-b)
                    if dist < prevDist:
                        prevDist = dist
                        name = key
                return (encircled, ((x,y),radius), name)
            
            
    
def name_characters():
    pass
            
def grid_draw(c):
    pass

input("Place PC's on the board.\nPress enter to contine...")




timeClk = 0
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

color1Lower = (0,0,167) #Background
color1Upper = (179,46,255) #Background

pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(1)
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    
#camera.set(3,480)
#camera.set(4,320)
printed = 0
numCharacters = 0
playerCharacters = {}
numconts = 0
font = cv2.FONT_HERSHEY_SIMPLEX

# keep looping
while True:
	# grab the current frame
    (grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask1 = cv2.inRange(hsv, color1Lower, color1Upper)
    mask1 = cv2.bitwise_not(mask1)
    mask1 = cv2.erode(mask1, None, iterations=10)
    mask1 = cv2.dilate(mask1, None, iterations=10)
    
    
        
   # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = []
    radius = []
 
    #cv2.circle(frame, (40, 20), int(10), (0,0,255), 2)
      
    #print(len(cnts1))
	# only proceed if at least one contour was found
    
    if len(cnts1) > 0 and numconts <= len(cnts1):
		# find the largest contour in the mask, then use.
		# it to compute the minimum enclosing circle and
		# centroid
        for i in range(0,len(cnts1)):
            outs = find_and_outline(cnts1[i],(255,0,0),printed,playerCharacters) 
            if outs == None:
                pass
            else:
                numCharacters = numCharacters+outs[0]
                playerCharacters[outs[2]]=outs[1]
        numconts = i
 
	# show the frame to our screen
    
    
    cv2.putText(frame,'test',(100,100), font, 1,(0,255,0),2,cv2.LINE_AA)
    
    for key in playerCharacters:
        x = int(playerCharacters[key][0][0])
        y = int(playerCharacters[key][0][1]-playerCharacters[key][1])
        cv2.putText(frame,key,(x,y), font, 1,(0,255,0),2,cv2.LINE_AA)
       
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    cv2.imshow("Mask",mask1)
 
	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    
    if printed == 0 and len(playerCharacters) > 0:
        print("There are " +str(numCharacters) + " PC's on the board")
        printed = 1



# cleanup the camera and close any open windows
cv2.destroyAllWindows()
camera.release()
