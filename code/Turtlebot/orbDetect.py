import cv2
import numpy as np
from matplotlib import pyplot as plt
from drawMatches import drawMatches

def getContours(frame):

	num2 = cv2.imread("number_two.jpg",cv2.IMREAD_GRAYSCALE)
	#bwframe = cv2.imread("number_two.jpg", cv2.IMREAD_GRAYSCALE) 
	bwframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	sift = cv2.SIFT()
	kp1, des1 = sift.detectAndCompute(num2, None)
	kp2, des2 = sift.detectAndCompute(bwframe, None)

	bf = cv2.BFMatcher()
	matches = bf.knnMatch(des1, des2, k=2)
	good = []
	for m,n in matches:
		if m.distance < .75 * n.distance:
			good.append([m])

	#img = cv2.drawKeypoints(frame, kp2)
	img3 = drawMatches(num2, kp1, bwframe, kp2, good)
	plt.imshow(img3), plt.show()
	cv2.imshow("blah",img)
	cv2.waitKey(0)
