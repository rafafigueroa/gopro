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
cntX = 0
while True:
	imgstr = camera.image()[21:];	
	imgraw = base64.decodestring(imgstr)
	pilImage = Image.open(StringIO.StringIO(imgraw));
	frame = np.array(pilImage)
	cv2.imshow('frame', frame)
	blueF = frame[:,:,0]
	greenF = frame[:,:,1]
	redF = frame[:,:,2]

	cv2.imshow('blue', blueF)
	cv2.imshow('green', greenF)
	cv2.imshow('red', redF)
	
	#bwframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	_, binf = cv2.threshold(redF, 250, 255, cv2.THRESH_BINARY)
	h, w = binf.shape

	ctrs0, hier = cv2.findContours(binf, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	M = cv2.moments(ctrs0[0])
	if M['m00'] != 0:
		cntX = int(M['m10']/M['m00'])
	print w/2 - cntX
	cv2.drawContours( binf, ctrs0, -1, (128, 255,255), 3)
	cv2.line(binf, (int(w/2),int(h/2)),(cntX, int(h/2)),[255,255,0]) 
	cv2.imshow('Dot', binf)
	


	#matImage = cv.fromarray(npImage)
	cv2.waitKey(1)
	
	#time.sleep(1)
