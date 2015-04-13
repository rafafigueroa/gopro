import cv2
import findTarget
import os


def rotate90(img):

        (h, w) = img.shape[:2]
        center = (w/2, h/2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(img, M, (w,h))
        return rotated

cap = cv2.VideoCapture(1)
count = 0
exposure = 150 
#logf = open("maxExp.txt","w")

while exposure < 180:
	print "Setting Exposure to " + str(exposure)
	setExp = "camControl/setExposure " + str(exposure)
	os.system(setExp)

	_,img = cap.read()
	img2 = rotate90(img)
	
	contours = findTarget.findTarget(img2)
	centers = findTarget.findCentroids(contours)
	if (len(centers) == 2):
		print len(centers), centers

	#logf.write("{0},{1}\n".format(exposure, len(centers)))

	exposure = exposure + 1
	#cv2.imshow("image", img2)
	cv2.waitKey(1)

