# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 20:27:12 2019

@author: uberg
"""

# import the necessary packages
from __future__ import print_function
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def order_points_old(pts):
    # initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect
	
def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points_old(pts)
    (tl, tr, br, bl) = rect
 
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    '''widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
 
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))'''
    
    maxHeight = 690
    maxWidth = 960
 
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
            [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
 
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
    # return the warped image
    return warped

def draw_grid(image):
    yPix,xPix,_ = image.shape
    numRows = 33
    numCols = 46
    rowOffset = 15
    colOffset = 15
    rowWidth = np.floor((yPix-rowOffset)/numRows)
    colWidth = np.floor((xPix-colOffset)/numCols)
    for i in range(0,numCols+1):
        cv2.line(image,(int(rowOffset+i*rowWidth),int(colOffset)),
                 (int(rowOffset+i*rowWidth),int(yPix-colOffset)),(255,0,0),1)
        
    for i in range(0,numRows+1):
        cv2.line(image,(int(rowOffset),int(colOffset+i*colWidth)),
                 (int(xPix-rowOffset),int(colOffset+i*colWidth)),(255,0,0),1)
    

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--new", type=int, default=-1,
	help="whether or not the new order points should should be used")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(2)
 
def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('Image')

while(1):
    
    _, image = cap.read()
    # Blur the images
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,np.array([0,0,88]),np.array([179,74,255]))
    
    gray = cv2.GaussianBlur(mask, (7, 7), 0)
    
    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=3)
    edged = cv2.erode(edged, None, iterations=3)
    
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # sort the contours from left-to-right and initialize the bounding box
    # point colors
    (cnts, _) = contours.sort_contours(cnts)
    colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
    
    # loop over the contours individually
    for (i, c) in enumerate(cnts):
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 200:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
 
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
        # compute the rotated bounding box of the contour, then
        # draw the contours
        '''box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")'''
    try:
        pts = screenCnt.reshape(4, 2)
        cv2.drawContours(image, [pts], -1, (0, 255, 0), 2)
        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        image = four_point_transform(image, pts)
        # check to see if the new method should be used for
        # ordering the coordinates
        if args["new"] > 0:
            rect = perspective.order_points(pts)
    except:
        pass
    
    
    

    
    # loop over the original points and draw them
    '''for ((x, y), color) in zip(rect, colors):
        cv2.circle(image, (int(x), int(y)), 5, color, -1)'''
    
    draw_grid(image)
    
    # show the image
    cv2.imshow("Image", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
        
cap.release()
 
cv2.destroyAllWindows()