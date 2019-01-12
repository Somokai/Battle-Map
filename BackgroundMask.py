import cv2
import numpy as np
from scipy import stats
 
cap = cv2.VideoCapture(2)
 
def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

colorMask =  np.array([0,0,0])
initialColorMask = colorMask
cropping = False
        
lower =  np.array([0,0,0])
upper =  np.array([179,255,255]) 

while(1):
 
    _, frame = cap.read()
 
    #converting to HSV
    hsv = np.array(cv2.cvtColor(frame,cv2.COLOR_BGR2HSV))
    h = hsv[:,:,0].reshape(hsv.shape[0]*hsv.shape[1])
    s = hsv[:,:,1].reshape(hsv.shape[0]*hsv.shape[1])
    v = hsv[:,:,2].reshape(hsv.shape[0]*hsv.shape[1])
    
    #hmode = stats.mode(h)
    #smode = stats.mode(s)
    vmode = stats.mode(v)

    #lower[0] = hmode[0]*0.8
    #lower[1] = smode[0]*0.8
    #print(vmode[0])
    lower[2] = vmode[0]*0.6

    
    mask = cv2.bitwise_not(cv2.inRange(hsv,lower, upper))
 
    result = cv2.bitwise_and(frame,frame,mask = mask)
    
    cv2.imshow('result',result)

    #print(colorMask)
    
 
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
cap.release()
 
cv2.destroyAllWindows()