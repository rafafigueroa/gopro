# Finds the countours by looking for the brightes object in the green frame.
import cv2
import numpy as np

def getContours(theframe):
	
	params= cv2.SimpleBlobDetector_Params()
	params.minThreshold = 245
	params.maxThreshold = 255
	params.filterByCircularity = True
	params.minCircularity = .8
	
	detector = cv2.SimpleBlobDetector(params)
        imgray = cv2.cvtColor( theframe, cv2.COLOR_BGR2GRAY)
	keypoints = detector.detect(imgray)

	im_kp = cv2.drawKeypoints(imgray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
        ctrs, hier = cv2.findContours(im_kp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(thresh, ctrs, -1, (255, 255, 255), 3)
        cv2.imshow('kps',im_kp)
        return ctrs

