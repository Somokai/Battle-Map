# import the necessary packages
from centroidtracker import CentroidTracker
import numpy as np
import cv2


# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)
 
# initialize the video stream and allow the camera sensor to warmup
cap = cv2.VideoCapture(1)

# sets the size of the frame to use
cap.set(3,1920)
cap.set(4,1080)

#color1Lower = (0,0,92) # battle map from separate webcam
#color1Upper = (143,71,255) # battle map from separate webcam

color1Lower = (0,0,128) # coffee table mask
color1Upper = (45,255,255) # coffee table mask


# initialize the character name dictionary
characterNames = {}

# initialize so that we know if a dot has been drawn on a character
circleDrawn = False


# this is turned on until all characters have been identified
addingCharacters = True


# loop over frames
while True:
    # read the next frame from the video stream and resize it
    _,frame = cap.read()
    #frame = imutils.resize(frame, width=1080)
     
    # if the frame dimensions are None, grab them
    if W is None or H is None:
        (H, W) = frame.shape[:2]
 
    # convert to hsv for masking purposed
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # construct a mask for the color of the battle grid, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask1 = cv2.inRange(hsv, color1Lower, color1Upper)
    # perform a bitwise_not to invert the mask
    #mask1 = cv2.bitwise_not(mask1)
    # perform an erode and dilate to get rid of all of the small noise features
    mask1 = cv2.erode(mask1, None, iterations=10)
    mask1 = cv2.dilate(mask1, None, iterations=10)
    # finds all of the different contours present in the image
    cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    
    # initialized the array we will use to contain all of our PC's, NPC's, 
    # Monsters etc
    rects = []
    
    # loop through the contours so we can pick out all of the characters
    for i in range(0, len(cnts)):
        
        # make a rectangle around the contour and find the corners
        rect = cv2.minAreaRect(cnts[i])
        box = cv2.boxPoints(rect)
        # find the diagonal points to use for calculating the centroid and
        # crossLength
        xstart = box[0][0]
        ystart = box[0][1]
        xend = box[3][0]
        yend = box[3][1]
        
        # calculates the diagonal to make sure our contours are not too big 
        # or small
        crossLength = np.sqrt((xstart-xend)**2+(ystart-yend)**2)
        
        # if the contours are the right size then append them to our rects
        # array.        
        if crossLength > 10 and crossLength < 500:
            rects.append((xstart, ystart, xend, yend))
            ##cv2.rectangle(frame, (xstart,ystart),(xend,yend),
            ##    (0,0,255), 1)
        
    
    # update our centroid tracker using the computed set of bounding
    # box rectangles
    objects = ct.update(rects)
 
    # loop over the tracked objects
    if len(characterNames) == len(objects) and len(characterNames) > 0:
            addingCharacters = False
     
    # here we check to see if characters are being added    
    if addingCharacters:
        for (objectID, centroid) in objects.items():
            # draw both the ID of the object and the centroid of the
            # object on the output frame             
            if objectID in characterNames:
                cv2.putText(frame, characterNames[objectID], (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1) 
            # because the dot won't get drawn on until the next frame we first 
            # draw the dot, then break the for loop
            elif not circleDrawn:
                    cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                    circleDrawn = True
                    break
            # once the dot is drawn then we get command line input to add in 
            # the character names.
            else:    
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                name = input("Who is this? ")
                characterNames[objectID] = name
                circleDrawn = False
    # if all of the characters have been added we simply keep updating them and
    # adding the dots to the frames
    else:
        for objectID in characterNames:
            try:
                centroid = objects[objectID]
                cv2.putText(frame, characterNames[objectID], (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            except:
                pass
            
                

    # display the mask
    cv2.imshow("Mask",mask1)
        
    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
# do a bit of cleanup
cv2.destroyAllWindows()
cap.release()