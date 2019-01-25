# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 11:25:35 2019

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
    cv2.rectangle(image, pt1, pt2, color,3)

        
def add_range_squares(reference,start,end,image,side):
    
    (row,col,_) = image.shape
    row = np.floor(row-(reference[0]-side/2))
    col = np.floor(col-(reference[1]-side/2))
    
    rise = int(end[0]-start[0])
    run = int(end[1]-start[1])
    clone[start[1]][start[0]] = (0,0,255)
    xPos = start[0]
    yPos = start[1]
    
    hitBox = np.zeros([int(row/side),int(col/side)])  

    #clone[yPos][xPos] = (0,0,255)
    
    delta = [1,1]
    if rise < 0:
        delta[0] = -1
        rise = -rise
    if run < 0:
        delta[1] = -1
        run = -run
    if run == 0:
        ratio = np.inf  
        run = np.inf
    else:
        ratio = rise/run
        
    while abs(xPos-start[0]) <= rise and abs(yPos-start[1]) <= run:
        
        if (yPos-start[1])==0:
            yPos = yPos+delta[1]
        if abs((xPos-start[0])/(yPos-start[1])) < ratio:
            xPos = xPos+delta[0]
        else:
            yPos = yPos+delta[1]
            
        #print(xPos,yPos)
        #clone[yPos][xPos] = (0,0,255)
        boxX = int((xPos-reference[0]-side/2)/side+1)
        boxY = int((yPos-reference[0]-side/2)/side+1)
        if boxX >= 0 and boxY >= 0 and boxX < hitBox.shape[0] and boxY < hitBox.shape[1]:
            hitBox[boxX][boxY] = 1
                
    for x in range(0,int(row/side)):
        for y in range(0,int(col/side)):
            if hitBox[int(x)][int(y)]==1:
                highlight_square(x,y,side,reference,image,(0,255,0))
    
def range_of_influence(event, x, y, flags, param):
    gridSize = 102
    location = (100,200)
    attackType = 'cube'
    distance = 5*gridSize
    startPoint=(121,120)
    global clone
    global prevClone
    if event == cv2.EVENT_LBUTTONDOWN:
        if x == location[0]:
            location[0] = location[0]+1
        if y == location:
            location[1] = location[1]+1
            
        deltaX = abs(x-location[0])
        deltaY = abs(y-location[1])
        theta = np.arctan(deltaY/deltaX)
        if x > location[0]:
            newX = int(location[0]+distance*np.cos(theta))
        else:
            newX = int(location[0]-distance*np.cos(theta))
        if y > location[1]:
            newY = int(location[1]+distance*np.sin(theta))
        else:
            newY = int(location[1]-distance*np.sin(theta))
            
        clone = prevClone

        if attackType == 'line':              
            add_range_squares(startPoint,location,(newX,newY),clone,gridSize)
            cv2.imshow('dst',clone)
                         
        # We need to fix the wrap around issue
        elif attackType == 'cone':  
            count = int(distance/gridSize)
            add_range_squares(startPoint,location,(newX,newY),clone,gridSize)

            for i in range(0,count):
                coneX = newX+(location[1]-newY)/(2+i)
                coneY = newY+(newX-location[0])/(2+i)
                add_range_squares(startPoint,location,(coneX,coneY),clone,gridSize)
                
                coneX = newX-(location[1]-newY)/(2+i)
                coneY = newY-(newX-location[0])/(2+i)
                add_range_squares(startPoint,location,(coneX,coneY),clone,gridSize)          
        
        elif attackType == 'sphere':
            count = 6
            x = int(round((x-startPoint[0]+gridSize)/gridSize)*gridSize+gridSize/4)
            y = int(round((y-startPoint[1]+gridSize)/gridSize)*gridSize+gridSize/4)
            for i in range(0,6*count):
                #print(2*np.pi*i/(2*count))
                newX = int(x+distance*np.cos(2*np.pi*i/(6*count)))
                newY = int(y+distance*np.sin(2*np.pi*i/(6*count)))
                print((x,y),(newX,newY))
                add_range_squares(startPoint,(x,y),(newX,newY),clone,gridSize)

        elif attackType == 'cube':
            x = int(round((x-startPoint[0]+gridSize)/gridSize)*gridSize+gridSize/4)
            y = int(round((y-startPoint[1]+gridSize)/gridSize)*gridSize+gridSize/4)
            for i in range(0,int(distance/gridSize)):
                newXNeg = int(x-distance/2+10)
                newXPos = int(x+distance/2-10)
                newY = int(y-distance/2+i*gridSize)
                add_range_squares(startPoint,(newXNeg,newY),(newXPos,newY),clone,gridSize)
                #cv2.circle(clone, (newXNeg,y),3,(0,0,255))
            
        elif attackType == 'cylinder':
            count = 6
            x = int(round((x-startPoint[0]+gridSize)/gridSize)*gridSize+gridSize/4)
            y = int(round((y-startPoint[1]+gridSize)/gridSize)*gridSize+gridSize/4)
            x = int((x+startPoint[0]-gridSize/2)/gridSize)*gridSize+int(gridSize/4)
            y = int((y+startPoint[1]-gridSize/2)/gridSize)*gridSize+int(gridSize/4)
            for i in range(0,6*count):
                #print(2*np.pi*i/(2*count))
                newX = int(x+distance*np.cos(2*np.pi*i/(6*count)))
                newY = int(y+distance*np.sin(2*np.pi*i/(6*count)))
                print((x,y),(newX,newY))
                add_range_squares(startPoint,(x,y),(newX,newY),clone,gridSize)
               # cv2.circle(clone,(newX,newY),5,(0,255,))
            
        elif attackType == 'melee':
            count = 6
            x = int((x+startPoint[0]-gridSize/2)/gridSize)*gridSize+int(gridSize/4)
            y = int((y+startPoint[1]-gridSize/2)/gridSize)*gridSize+int(gridSize/4)
            for i in range(0,6*count):
                #print(2*np.pi*i/(2*count))
                newX = int(x+distance*np.cos(2*np.pi*i/(6*count)))
                newY = int(y+distance*np.sin(2*np.pi*i/(6*count)))
                print((x,y),(newX,newY))
                add_range_squares(startPoint,(x,y),(newX,newY),clone,gridSize)
                #cv2.circle(clone,(newX,newY),5,(0,255,))

 
filename = 'test-scale-reference.jpg'
img = cv2.imread('test.jpg')
cv2.namedWindow("dst")
clone = img.copy()
cv2.setMouseCallback("dst", range_of_influence)


while True:
    
    refImg = cv2.imread(filename)
    gray = cv2.cvtColor(refImg,cv2.COLOR_BGR2GRAY)
    
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
    gridSize = np.floor((sizeOfRect[0]+sizeOfRect[1])/2)+1

    prevClone = img.copy()
    cv2.imshow('dst',clone)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()