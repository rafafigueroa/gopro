import cv2.cv as cv

cap = cv.CaptureFromCAM(1)
count = 0
while True:
	img = cv.QueryFrame(cap)
	count = count + 1
	print count
	cv.ShowImage("test", img)
	cv.WaitKey(0)

	
