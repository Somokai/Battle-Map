import cv2
import numpy as np
 
 
cap = cv2.VideoCapture(2)
 
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

 
while(1):
 
    _, frame = cap.read()
 
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 
    # get info from track bar and appy to result
    hl = cv2.getTrackbarPos('hl','result')
    sl = cv2.getTrackbarPos('s','result')
    vl = cv2.getTrackbarPos('v','result')
    hu = cv2.getTrackbarPos('hu','result')
    su = cv2.getTrackbarPos('su','result')
    vu = cv2.getTrackbarPos('vu','result')

 
    # Normal masking algorithm
    lower_blue = np.array([hl,sl,vl])
    upper_blue = np.array([hu,su,vu])
 
    mask = cv2.inRange(hsv,lower_blue, upper_blue)
 
    result = cv2.bitwise_and(frame,frame,mask = mask)
 
    cv2.imshow('result',result)
 
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
cap.release()
 
cv2.destroyAllWindows()