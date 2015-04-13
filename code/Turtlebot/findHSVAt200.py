import cv2
import findTarget
import os
import numpy as np


def rotate90(img):

        (h, w) = img.shape[:2]
        center = (w/2, h/2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(img, M, (w,h))
        return rotated

def setExposure(exposure):
	print "Setting Exposure to " + str(exposure)
	setExp = "camControl/setExposure " + str(exposure)
	os.system(setExp)

def centersInRange(centers):
	if (len(centers) > 2):
		return False
	if (len(centers) < 2):
		return False
	x1 = centers[0][0]
	y2 = centers[0][1]
	x2 = centers[1][0]
	y2 = centers[1][1]
	print "2 Centers: " + str(centers)
	if x1 in range(478, 488) and y1 in range(225, 235):
		if x2 in range(484, 494) and y2 in range(219, 229):
			return True
	if x2 in range(478, 488) and y2 in range(225, 235):
		if x1 in range(484, 494) and y1 in range(219, 229):
			return True
	return False


cap = cv2.VideoCapture(1)
count = 0
logf = open(".txt","w")


setExposure(160)
_,img = cap.read()
img2 = rotate90(img)
	
for lows  in range(249,254, 5):
	for highs in range(lows, 255, 5):
		#fname="40_{0}_50_60_{1}_255.txt".format(lows, highs)
		lowHSV = np.array((40,lows,50))
		highHSV = np.array((50,highs,50))
		contours = findTarget.findTarget(img2) #, lowHSV, highHSV)
		centers = findTarget.findCentroids(contours)
		print len(centers)
		print centers
		#print "Checking " + str(lows) + str(highs)
		if len(centers) == 2:
			#print contours
			print centers
			cv2.waitKey(0)
		if centersInRange(centers):
			print "			" + str(lows) + " " + str(highs) + " " + str(len(centers))
	
		

