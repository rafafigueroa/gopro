import cv2
import numpy as np
from goprohero import GoProHero
from PIL import Image
import cv
import base64
import time
import StringIO 

red_low = np.array([0,100,100])
red_high = np.array([40,255,255])

def nothing(*arg):
	pass

cv2.namedWindow("Adjust")
cv2.createTrackbar("H Upper","Adjust",0, 255, nothing)
#cv2.createTrackbar("S Upper","Adjust",0, 255, nothing)
#cv2.createTrackbar("V Upper","Adjust",0, 255, nothing)
#cv2.createTrackbar("H Lower","Adjust",0, 255, nothing)
#cv2.createTrackbar("S Lower","Adjust",0, 255, nothing)
#cv2.createTrackbar("V Lower","Adjust",0, 255, nothing)

cv2.namedWindow("Image")
cv2.namedWindow("Result")
cv2.namedWindow("Mask")

camera = GoProHero(password = 'rafadrone')
camera.command('fov','90')
#camera.command('picres','12MP wide')
while True:

	imgstr = camera.image()[21:]
	imgraw = base64.decodestring(imgstr)
	pilImg = Image.open(StringIO.StringIO(imgraw))
	frame = np.array(pilImg)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#mask = cv2.inRange(hsv, red_low, red_high)
	mask = cv2.threshold(gray, red_high[0], 1, cv2.THRESH_BINARY)
	#res = cv2.bitwise_and(frame, frame, mask = mask)
	cv2.imshow('Image', frame)
	cv2.imwrite('image.png',frame)
	#cv2.imshow('Mask', mask)
	#cv2.imshow('Result', res)
	
	red_high[0] = cv2.getTrackbarPos("H Upper","Adjust")
	#red_high[1] = cv2.getTrackbarPos("S Upper","Adjust")
	#red_high[2] = cv2.getTrackbarPos("V Upper","Adjust")
	#red_low[0] = cv2.getTrackbarPos("H Lower","Adjust")
	#red_low[1] = cv2.getTrackbarPos("S Lower","Adjust")
	#red_low[2] = cv2.getTrackbarPos("V Lower","Adjust")
	
	# cv2.imsave('image.png', frame)
	cv2.waitKey(1)

cv2.destroyAllWindows()



cv2.waitKey(0)
 
	
