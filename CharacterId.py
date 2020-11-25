import numpy as np 
import cv2

A = np.array([1,2,3,4,5,6,7,8])
A = A/np.sum(A)
B = np.array([5,1,5,6,2,5,6,3])
B = B/np.sum(B)

C = A

D = np.correlate(A,B)
E = np.correlate(A,A)
print(D,E)


# Read image
im = cv2.imread("testSingle.jpg", cv2.IMREAD_GRAYSCALE)

th, thresh1 = cv2.threshold(im, 220, 255, cv2.THRESH_BINARY_INV);
small_to_large_image_size_ratio = 0.1
small_img = cv2.resize(im, # original image
                       (0,0), # set fx and fy, not the final size
                       fx=small_to_large_image_size_ratio, 
                       fy=small_to_large_image_size_ratio, 
                       interpolation=cv2.INTER_NEAREST)

kernel = np.ones((10,10),np.float32)/(100)
small_img = cv2.filter2D(small_img,-1,kernel)


params = cv2.SimpleBlobDetector_Params()
params.filterByColor = True;
params.filterByCircularity = False;
params.filterByConvexity = False;

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
keypoints = detector.detect(small_img)
    

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = im
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
edgePoints = np.where(edges == 255)
print(edgePoints)
angles = np.zeros((len(edgePoints[0]),1))
for pInd in range(len(edgePoints[0])):
    dx = edgePoints[0][pInd]-x
    dy = edgePoints[1][pInd]-y
    angles[pInd] = np.arctan(dx/dy)

print(angles)    

# Show keypoints
cv2.imshow("smallImg",small_img)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.imshow("image",thresh1)
cv2.imshow("Thresholded Image", thresh1)
cv2.imshow("Floodfilled Image", im_floodfill)
cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
cv2.imshow("Foreground", im_out)
cv2.imshow("Edges",edges)
cv2.waitKey(0)