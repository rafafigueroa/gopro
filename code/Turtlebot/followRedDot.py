from __future__ import division
import base64
import numpy as np
import cv2
import cv
from PIL import Image
import StringIO
from goprohero import GoProHero
import time
import os

def drawAxis(aframe):

	h,w = aframe.shape[:2]
	h2 = int(h/2)
	w2 = int(w/2)
	#X-axis
	cv2.line(aframe, (w2,h2),(w2 + 50,h2),[255,0,0], thickness = 4)
	#Y-axis
	cv2.line(aframe, (w2,h2),(w2,h2-50), [0,255,0], thickness = 4)


def controlLaw( y, ref ):
	if 'y' in locals():
		k = .25 
		spd = -k * (  y - ref   )
		if spd < 0:
			spdString = "   %s" % spd 
		else:
			spdString = "   +%s" % spd
		print "Loc:",y,"   String:",spdString
		os.system("echo '%s' > /dev/ttyUSB0" % spdString)

def getFrame():
	imgstr = camera.image()[21:];	
	imgraw = base64.decodestring(imgstr)
	pilImage = Image.open(StringIO.StringIO(imgraw));
	frame = np.array(pilImage)
	return frame

def findTheDot(theframe):	
	imgray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(imgray, 240, 255, cv2.THRESH_BINARY)
	
	ctrs, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(thresh, ctrs, -1, (255, 255, 255), 3)
	cv2.imshow('threshold',thresh)
	return ctrs


camera = GoProHero(password='rafadrone')
camera.command('fov','90')
#camera.command('mode','still')
camera.command('picres','12MP wide')
#camera.command('record','off')

while True:
	frame = getFrame()

	h, w = frame.shape[:2]
	ref = h/2
	ctrs = findTheDot(frame)	

	if len(ctrs) <= 0:
		print "Contours not found!"
		continue
	
	M = cv2.moments(ctrs[0])
	if M['m00'] != 0:
		cntX = int(M['m10']/M['m00'])
		cntY = int(M['m01']/M['m00'])
	else:
		cntY = ctrs[0][0][0][1]

	drawAxis(frame)	
	#cv2.line(frame,int((w/2,h/2)),int(w/2+50,h/2)),[0,0,255],thickness = 4)
	#cv2.line(frame,int((w/2,h/2)),int((w/2, h/2-50)),[255,0,0],thickness = 4) 

	controlLaw(cntY, ref)

	cv2.imshow('frame', frame)
	cv2.waitKey(1)


	
