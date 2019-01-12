# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 14:37:07 2019

@author: uberg
"""
import cv2
import numpy as np
import imutils

def highlight_square(row,col,side,reference, image):
    rowLoc = 0
    colLoc = 0
    for i in range(0,row):
        rowLoc = reference[0]+side
        
    for j in range(0,col):
        colLoc = reference[0]+side
        
    cv2.rectangle(image, pt1, pt2, color[, thickness[, lineType[, shift]]]) 

filename = 'test-scale-reference.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray[gray<250] = 0
cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
gray = np.float32(gray)

cv2.imshow('dst',gray)

dst = cv2.cornerHarris(gray,2,3,0.04)

cnts = imutils.grab_contours(cnts)
    
# sort the contours from left-to-right and initialize the bounding box
# point colors
c = max(cnts, key=cv2.contourArea)
startPoint, sizeOfRect, rot = cv2.minAreaRect(c)
cv2.line(img,(326, 528), (326+int(100/2), 528+int(102/2)),(0,255,0))
gridSize = np.floor((sizeOfRect[0]+sizeOfRect[1])/2)
print(gridSize)
 
#result is dilated for marking the corners, not important
'''dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()'''