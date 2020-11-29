# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:03:21 2020

@author: zacha
"""
def extractSilhouette(imgName):
    import numpy as np 
    import cv2
    import matplotlib.pyplot as plt

    # Read image
    if isinstance(imgName,str):
        im = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
        im = cv2.rotate(im,cv2.ROTATE_180)
        im = im[300:700,380:800]
        im = cv2.flip(im,1)
    else:
        im = imgName
            
    small_to_large_image_size_ratio = 0.1
    small_img = cv2.resize(im, # original image
                           (0,0), # set fx and fy, not the final size
                           fx=small_to_large_image_size_ratio, 
                           fy=small_to_large_image_size_ratio, 
                           interpolation=cv2.INTER_NEAREST)
    th, thresh1 = cv2.threshold(im, 150, 255, cv2.THRESH_BINARY_INV);
    
    kernel = np.ones((10,10),np.float32)/(100)
    small_img = cv2.filter2D(small_img,-1,kernel)
    
    
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = True;
    params.filterByCircularity = False;
    params.filterByConvexity = False;
    
    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)
    
    #Lenght of output signal
    dataLen = 200
    
    # Detect blobs.
    keypoints = detector.detect(small_img)
        
    
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = im.copy()
    for i in range(len(keypoints)):
        x = np.int(keypoints[i].pt[0]/small_to_large_image_size_ratio)
        y = np.int(keypoints[i].pt[1]/small_to_large_image_size_ratio)
        radius = np.int(keypoints[i].size/small_to_large_image_size_ratio/2)
        cv2.circle(im_with_keypoints,(x,y),radius,(0,255,0))
    
    
    im_floodfill = thresh1.copy();
    h, w = thresh1.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = thresh1 | im_floodfill_inv
    
    
     
    edges = np.array(cv2.Canny(im_out,im.shape[0],im.shape[1]))
    edgePoints = np.array(np.where(edges == 255))
    #print(edgePoints)
    numPoints = len(edgePoints[0])
    '''cv2.imshow("smallImg",small_img)
    cv2.imshow("Keypoints", im_with_keypoints)
    cv2.imshow("image",thresh1)
    cv2.imshow("Thresholded Image", thresh1)
    cv2.imshow("Floodfilled Image", im_floodfill)
    cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
    cv2.imshow("Foreground", im_out)
    cv2.imshow("Edges",edges)
    cv2.waitKey(0)'''
    
    if numPoints == 0 or not keypoints:
    
        finSig = np.ones(dataLen)
        print('I got Nuttin')
    else:
                
        # print(angles)  
        
        # Sort the data into a reasonable order, we begin by first 
        availablePts = np.array(range(1,numPoints))
        orderedPts = np.zeros((2,numPoints))
        currentPoint = edgePoints[:,0]
        orderedPts[:,0] = currentPoint
        for edgeInd in range(1,len(edgePoints[0])):
            dx = currentPoint[0]-edgePoints[0,:]
            dy = currentPoint[1]-edgePoints[1,:]
            distances = np.abs(np.sqrt(np.square(dx)+np.square(dy)))
            # Pickout things within 1 pixel of the current point
            minDist = np.array(np.where(distances == min(distances[availablePts])))
            inds = np.where(np.in1d(minDist, availablePts))[0]
            minDist = minDist[0,inds[0]]
    
            if isinstance(minDist,np.int64):
                thisOne = minDist 
            elif minDist[0].size > 0:
                thisOne = minDist[0]
            else: 
                print('Somethin Broke')
                break        
            
            removeInd = np.where(availablePts == thisOne)
            availablePts = np.delete(availablePts,removeInd[0])
            orderedPts[:,edgeInd] = edgePoints[:,thisOne]
            currentPoint = edgePoints[:,thisOne]
           # print(currentPoint)
            '''plt.imshow(edges)
            plt.scatter(orderedPts[1,0:edgeInd+1],orderedPts[0,0:edgeInd+1])
            #plt.plot(signal)
            plt.show()'''
    
        # Extract the signal
        signal = np.zeros(numPoints)
        if orderedPts[0,0] < orderedPts[0,4]:
            orderedPts = np.flip(orderedPts,0)
        dx = x - orderedPts[0,:]
        dy = y - orderedPts[1,:]
        signal = np.sqrt(np.square(dx)+np.square(dy))
        
        # Smooth the signal
        boxPts = 5
        box = np.ones(boxPts)/boxPts
        smoothedSig = np.convolve(signal, box, mode='same')
        smoothedSig = smoothedSig[boxPts-1:numPoints-boxPts-1]
        
        xSig = np.linspace(0,1,len(smoothedSig))
        xp = np.linspace(0,1,dataLen)
        finSig = np.interp(xp,xSig,smoothedSig)
        '''plt.imshow(edges)
        plt.scatter(orderedPts[:,0],orderedPts[:,1])'''
        
    
    return finSig/np.sum(finSig), edges


# Show keypoints
   