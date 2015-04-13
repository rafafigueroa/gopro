from __future__ import division
import cv2
import cv
import numpy as np

def rotate90(img):

        (h, w) = img.shape[:2]
        center = (w/2, h/2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(img, M, (w,h))
        return rotated

def findCentroids(contours):
	centers = []
	for n in contours:
		M = cv2.moments(n)
		if M['m00'] <> 0:
			cx = ( int(M['m10'] / M['m00']))
			cy = ( int(M['m01'] / M['m00']))
		else:
			cx = ( int(M['m10']))
			cy = ( int(M['m01']))
		centers.append([cx,cy])
	return centers 
	
		
def findTarget(img, low = np.array((40,50,50)), high = np.array((60,255,255))):
	# Tries to locate the turtlebot using blobs
	# Turtlebot has 2 sets of LEDs. One on the back, the other on the top.
	# If we can see the "top" LED we should see 2 of them.

	#params = cv2.SimpleBlobDetector_Params()

	#params.minThreshold = 1;
	#params.maxThreshold = 255;
 
    #get the brightness mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsvmask = cv2.inRange(hsv,low , high)
    hsvMasked = cv2.bitwise_and(img, img, mask = hsvmask)
    img1 = hsvMasked[:,:,2]
    #_, bmask = cv2.threshold(hsvMasked, 240, 255, )
    # Convert to grayscale
    #graymask = cv2.cvtColor(bmask, cv2.COLOR_BGR2GRAY)
    # close
    #img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret, img2 = cv2.threshold(img1, 220, 255, 0)
    kernel = np.ones((3,3),np.uint8)
    #opened = cv2.morphologyEx(graymask, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(img1, cv2.MORPH_CLOSE, kernel)
    # Now use the closed to mask out the original image
    #_, mask = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY)
    #maskedByBrightness = cv2.bitwise_and( img, img, mask = mask)
    #hsvmaskedimg = cv2.cvtColor(maskedByBrightness, cv2.COLOR_BGR2HSV)

    #hsvClosed = cv2.morphologyEx(hsvmask, cv2.MORPH_OPEN, np.ones((1,1), np.uint8), 2)
    #hsvDil = cv2.dilate(hsvClosed, np.ones((3,3), np.uint8), 2)
    #cv2.imshow("hsv Dil", hsvmask)

    #maskedImg = cv2.bitwise_and( img, img, mask = hsvDil)
    #cv2.imshow("orig", img)
    #cv2.imshow("Masked Image", maskedImg)
    
    ctrs = [] 
    ctrs, hier = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return ctrs

	 
 
# Show keypoints
	#cv2.imshow("Keypoints", img)
#	cv2.waitKey(0)

#cap = cv2.VideoCapture(1)
#cntrs = findTarget(cap)
#findCentroids(cntrs)

