import numpy as np
import cv2

cap = cv2.VideoCapture(1)
framesCaped = 0

while (True):
	ret, frame = cap.read()
	cv2.imshow("Frame",frame)
	cv2.waitKey(1)
	framesCaped = framesCaped + 1
	print framesCaped

