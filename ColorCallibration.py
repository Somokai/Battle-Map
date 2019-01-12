import cv2
import numpy as np
import argparse
 
 
cap = cv2.VideoCapture(1)

 
def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')
 
# Starting with 100's to prevent error while masking
hl,s,v,hu = 100,100,100,180
 
# Creating track bar
cv2.createTrackbar('hl', 'result',0,179,nothing)
cv2.createTrackbar('sl', 'result',0,255,nothing)
cv2.createTrackbar('vl', 'result',0,255,nothing)
cv2.createTrackbar('hu', 'result',0,179,nothing)
cv2.createTrackbar('su', 'result',0,255,nothing)
cv2.createTrackbar('vu', 'result',0,255,nothing)

colorMask =  np.array([0,0,0])
initialColorMask = colorMask

refPt = []
cropping = False
 
def get_click_hsv(event, x, y, flags, param):
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed

	# check to see if the left mouse button was released
    if event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
        framehsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        h = framehsv[y,x,0]
        s = framehsv[y,x,1]
        v = framehsv[y,x,2]
        #print(h,s,v)
        global colorMask
        colorMask = np.array([h,s,v])
        
lower =  np.array([0,0,0])
upper =  np.array([179,255,255]) 

while(1):
 
    _, frame = cap.read()
    #frame = cv2.imread('BattleMapTest.jpeg')
 
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 
    # Normal masking algorithm
    '''lower_blue = np.array([hl,sl,vl])
    upper_blue = np.array([hu,su,vu])'''
    #print(colorMask)
    #print(initialColorMask)
    '''if colorMask[0]==initialColorMask[0] and colorMask[1]==initialColorMask[1] and colorMask[2]==initialColorMask[2]:
        pass
    else:
        #print('Got Here')
        for col in range(len(colorMask)):
            lower[col] = colorMask[col]*0.7
        for col in range(len(colorMask)):
            upper[col] = colorMask[col]*1.5
            

    # get info from track bar and appy to result
    cv2.setTrackbarPos('hl','result',lower[0])
    cv2.setTrackbarPos('sl','result',lower[1])
    cv2.setTrackbarPos('vl','result',lower[2])
    cv2.setTrackbarPos('hu','result',upper[0])
    cv2.setTrackbarPos('su','result',upper[1])
    cv2.setTrackbarPos('vu','result',upper[2])'''
    
    lower[0] = cv2.getTrackbarPos('hl','result')
    lower[1] = cv2.getTrackbarPos('sl','result')
    lower[2] = cv2.getTrackbarPos('vl','result')
    upper[0] = cv2.getTrackbarPos('hu','result')
    upper[1] = cv2.getTrackbarPos('su','result')
    upper[2] = cv2.getTrackbarPos('vu','result')

    mask = cv2.inRange(hsv,lower, upper)
 
    result = cv2.bitwise_and(frame,frame,mask = mask)
    
    cv2.setMouseCallback('result', get_click_hsv)
    cv2.imshow('result',result)

    #print(colorMask)
    
 
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
cap.release()
 
cv2.destroyAllWindows()

print(lower,upper)