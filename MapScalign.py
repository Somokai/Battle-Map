# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 14:37:07 2019

@author: uberg
"""
import cv2
import numpy as np
import imutils

def highlight_square(x,y,side,reference, image,color):
    xLoc = reference[0]
    yLoc = reference[1]
    for i in range(0,x):
        xLoc = xLoc+side
        
    for j in range(0,y):
        yLoc = yLoc+side
        
    offset = np.floor(side/2)
        
    pt1 = (int(xLoc-offset),int(yLoc-offset))
    pt2 = (int(xLoc+offset),int(yLoc+offset))
        
    cv2.rectangle(image, pt1, pt2, color,-1) 

filename = 'test-scale-reference.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray[gray<250] = 0
cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
gray = np.float32(gray)

#cv2.imshow('dst',gray)

dst = cv2.cornerHarris(gray,2,3,0.04)

cnts = imutils.grab_contours(cnts)
    
# sort the contours from left-to-right and initialize the bounding box
# point colors
c = max(cnts, key=cv2.contourArea)
startPoint, sizeOfRect, rot = cv2.minAreaRect(c)
#cv2.line(img,(326, 528), (326+int(100/2), 528+int(102/2)),(0,255,0))
img = cv2.imread('test.jpg')
gridSize = np.floor((sizeOfRect[0]+sizeOfRect[1])/2)+1
print(gridSize)

highlight_square(3,5,gridSize,startPoint,img,(0,255,0))
highlight_square(10,3,gridSize,startPoint,img,(255,0,0))
highlight_square(5,7,gridSize,startPoint,img,(0,255,255))
highlight_square(15,15,gridSize,startPoint,img,(0,0,255))


cv2.imshow('dst',img)
cv2.waitkey()
 