import base64
import numpy as np
import cv2
import cv
from PIL import Image
import StringIO
from goprohero import GoProHero
import time

camera = GoProHero(password='rafadrone')
#camera.command('fov','170')
#camera.command('mode','still')
#camera.command('picres','5MP wide')
camera.command('record','off')

#imgstr = open("testimage.txt","rb").read()

while True:
	imgstr = camera.image()[21:]	
#	open("test.txt","w").write(imgstr).close()
	imgraw = base64.decodestring(imgstr)
	pilImage = Image.open(StringIO.StringIO(imgraw));
	frame = np.array(pilImage)
	hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

	red = np.uint8([[0,0,255]])	
	lower_red = np.array([0, 100, 100])
	upper_red = np.array([40, 255, 255])
	mask = cv2.inRange(hsv, lower_red, upper_red)
	res = cv2.bitwise_and(frame, frame, mask = mask)
	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('res', res)

	#matImage = cv.fromarray(npImage)
	cv2.waitKey(1)
	
	#time.sleep(1)
