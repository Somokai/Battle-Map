# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 17:40:20 2019

@author: uberg
"""

import cv2
import numpy as np
import imutils


while True:
    
    img = cv2.imread('BattleMapTest.jpeg')
    refImg = cv2.imread('test-scale-reference.jpg')
    
    rowBM,colBM,_ = img.shape
    cv2.circle(img,(38,26),5,(0,255,0),2)
    cv2.circle(img,(38,64),5,(0,255,0),2)
    cv2.circle(img,(57,45),5,(0,255,0),2)
        
    gray = cv2.cvtColor(refImg,cv2.COLOR_BGR2GRAY)
    
    gray[gray<250] = 0
    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL,
        	cv2.CHAIN_APPROX_SIMPLE)
    gray = np.float32(gray)
    
    #cv2.imshow('dst',gray)
    row,col,_ = refImg.shape
    
    dst = cv2.cornerHarris(gray,2,3,0.04)
    
    cnts = imutils.grab_contours(cnts)
        
    # sort the contours from left-to-right and initialize the bounding box
    # point colors
    c = max(cnts, key=cv2.contourArea)
    startPoint, sizeOfRect, rot = cv2.minAreaRect(c)
    gridSize = np.floor((sizeOfRect[0]+sizeOfRect[1])/2)+1
    
    startPointBM = (57,45)
    gridSizeBM = 38

    rowOffset = int(gridSizeBM/gridSize*startPoint[0])
    colOffset = int(gridSizeBM/gridSize*startPoint[1])
     
    
    alpha = 0.8
    beta = 1-alpha
    
    #cv2.namedWindow('blended',1)
    refImg = cv2.resize(refImg,(int(gridSizeBM/gridSize*col)-1,int(gridSizeBM/gridSize*row)))
    xPad = int((rowBM-refImg.shape[0])/2)
    yPad = int((colBM-refImg.shape[1])/2)
    refImg = cv2.copyMakeBorder(refImg,xPad+rowOffset,xPad-rowOffset,yPad+colOffset,yPad-colOffset,cv2.BORDER_CONSTANT,value=(255,255,255))
    dst = cv2.addWeighted(img,alpha,refImg,beta,0)


    cv2.imshow('blended',dst)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()