import cv2
from orbDetect import getContours


def rotate90(img):

        (h, w) = img.shape[:2]
        center = (w/2, h/2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        rotated = cv2.warpAffine(img, M, (w,h))
        return rotated

cap = cv2.VideoCapture(1)

count = 0
while True:
	_,img = cap.read()
	img2 = rotate90(img)
	#getContours(img2)
	fname = "pic" + str(count) + ".png"
	cv2.imwrite(fname, img2)
	cv2.imshow("image", img2)
	print "Image saved..."
	count = count + 1
	cv2.waitKey(0)
	break;

