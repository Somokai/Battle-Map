# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import win32api, win32con
import time
 
def mv_chk(xPos, yPos, current):
    xAv = 0
    yAv = 0
    for item in xArr:
        xAv = item + xAv
    for item in yArr:
        yAv = item + yAv
    xAv = xAv/10
    yAv = yAv/10
    if np.sqrt((xAv-current[0])**2 + (yAv-current[1])**2) < 10:
        xNew = current[0]
        yNew = current[1]
    else:
        xNew = xAv
        yNew = yAv
    return (xNew,yNew)

def relative_lower(elem):
    return elem[1]+elem[1]*elem[0]
    
def find_and_outline(c, color):
        
        ((x, y), radius) = cv2.minEnclosingCircle(c)
 
		# only proceed if the radius meets a minimum size
        if radius > 5 and radius < 50:
            #print(c.shape)
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                color, 2)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            return [center,radius]
            #cv2.circle(frame, center1, 5, (50, 50, 255), -1)
            
def grid_draw(c):
    pass

timeClk = 0
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#color1Lower = (59, 93, 168) #green
#color1Upper = (96, 255, 255) #green
#color1Lower = (150, 122, 141) #hot pink
#color1Upper = (174, 255, 255) #hot pink
#color2Lower = (0, 122, 194) #blue
#color2Upper = (47, 255, 255) #blue
color2Lower = (60, 71, 75) #red poker chip
color2Upper = (158, 255, 255) #red poker chip
color1Lower = (1, 192, 50) #blue poker chip
color1Upper = (23, 255, 255) #blue poker chip
#color1Lower = (0, 0, 0) #white battle mat
#color1Upper = (179, 255, 100) #white battle mat
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(2)
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    
camera.set(3,1920)
camera.set(4,1080)

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
    mask1 = cv2.erode(mask1, None, iterations=4)
    mask1 = cv2.dilate(mask1, None, iterations=4)
    
    mask2 = cv2.inRange(hsv, color2Lower, color2Upper)
    mask2 = cv2.erode(mask2, None, iterations=4)
    mask2 = cv2.dilate(mask2, None, iterations=4)
    	# find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = []
    radius = []
 
    cv2.circle(frame, (40, 20), int(10), (0,0,255), 2)
      
    if len(cnts2) == 4:
        for i in range(0,len(cnts2)):
            pars = find_and_outline(cnts2[i],(0,0,255))
            center.append(pars[0])
            radius.append(int(pars[1]))
            print(i)
        
        radius = int(np.mean(radius))
        center.sort(key = relative_lower)
    
        cv2.line(frame, (center[1][0]-radius,center[1][1]+radius), (center[0][0]-radius,center[0][1]-radius), (0,255,0), 1)
        cv2.line(frame, (center[3][0]+radius,center[3][1]+radius), (center[2][0]+radius,center[2][1]-radius), (0,255,0), 1)
        cv2.line(frame, (center[2][0]+radius,center[2][1]-radius), (center[0][0]-radius,center[0][1]-radius), (0,255,0), 1)
        cv2.line(frame, (center[1][0]-radius,center[1][1]+radius), (center[3][0]+radius,center[3][1]+radius), (0,255,0), 1)

        rows,cols,nada = frame.shape
    
        newShape = np.array([[0,0],[0,584],[800,0],[800,584]],np.float32)
        M = cv2.getPerspectiveTransform(np.array(center,np.float32),newShape)
        frame = cv2.warpPerspective(frame,M,(800,584))
        #ang = np.arctan(np.abs(((center[1][0])-(center[0][0])))/np.abs(((center[1][1])-(center[0][1]))))*180/np.pi
        '''M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
        frame = cv2.warpAffine(frame,M,(cols,rows))'''

	# only proceed if at least one contour was found
    if len(cnts1) > 0:
        xArr = []
        yArr = []
		# find the largest contour in the mask, then use.
		# it to compute the minimum enclosing circle and
		# centroid
        for i in range(0,len(cnts1)):
            find_and_outline(cnts1[i],(255,0,0))
            
        
        c = max(cnts1, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center1 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        
        xArr.append(center1[0])
        yArr.append(center1[1])
        
        size = 1000
        
        point = (abs(size-center1[0]),center1[1])
        
        if len(xArr) == 10:
            point = mv_check(xArr, yArr, center1)
            rem(xArr[0])
            rem(yArr[0])            
        
    	# loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is (0,0) or pts[i] is (0,0):
            continue
 
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
cv2.destroyAllWindows()
camera.release()
