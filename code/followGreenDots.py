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
import matplotlib.pyplot as plt
	
def drawAxis(aframe):

	h,w = aframe.shape[:2]
	h2 = int(h/2)
	w2 = int(w/2)
	#X-axis
	cv2.line(aframe, (w2,h2),(w2 + 50,h2),[0,0,255], thickness = 4)
	#Y-axis
	cv2.line(aframe, (w2,h2),(w2,h2-50), [255,0,0], thickness = 4)

def rotate90(img):

	(h, w) = img.shape[:2]
	center = (w/2, h/2)
	M = cv2.getRotationMatrix2D(center, -90, 1.0)
	rotated = cv2.warpAffine(img, M, (w,h))
	return rotated

def controlLaw( x,y, refx, refy ):
	print "X:",x,"  Ref:",refx
	k = .15 
	spd = -k * (  refx - x )
	if spd < 0:
		spdString = "   %s" % spd 
	else:
		spdString = "   +%s" % spd
	print "Loc:",x,"   String:",spdString
	os.system("echo '%s' > /dev/ttyUSB0" % spdString)
	xVals.append(x)
	yVals.append(y)
	logStr = "X Actual: " + str(x) + "X Reference: " + str(refx) + "\n"
	f.write(logStr)

def getFrame():
	img = camera.imageRaw();
	#cimg = np.array(pilImg) 
	rotframe = rotate90(img)
	
	#frame = np.array(pilImage)
	#rotframe = rotate90(frame)
	return rotframe

def findTheDot(theframe):
	greenF = frame[:,:,1]	
	#imgray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
	
	_, thresh = cv2.threshold(greenF, 225, 255, cv2.THRESH_BINARY)
	
	ctrs, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(thresh, ctrs, -1, (255, 255, 255), 3)
	cv2.imshow('threshold',thresh)
	return ctrs

def findCenter(contours):

	if len(contours) <= 1:
		print "2 Contours not found!"
		return -1000, -1000;	
	
	M1 = cv2.moments(ctrs[0])
	M2 = cv2.moments(ctrs[1])

	if M1['m00'] != 0:
		cntX1 = int(M1['m10']/M1['m00'])
		cntY1 = int(M1['m01']/M1['m00'])
	else:
		cntX1 = ctrs[0][0][0][0]
		cntY1 = ctrs[0][0][0][1]
	if M2['m00'] != 0:
		cntX2 = int(M2['m10']/M2['m00'])
		cntY2 = int(M2['m01']/M2['m00'])
	else:
		cntX2 = ctrs[1][0][0][0]
		cntY2 = ctrs[1][0][0][1]

	centerX = abs(int((cntX2 - cntX1) / 2)) + min(cntX1, cntX2)
	centerY = abs(int((cntY2 - cntY1) / 2)) + min(cntY1, cntY2)
	print "CX: ", centerX, "CY: ", centerY
	return centerX, centerY

def plotVals(xvals, yvals, xref, yref):

	fig, ax = plt.subplots()
	ax.plot(xvals,label = 'X Position', linewidth = 4)
	xr = [xref] * len(xvals)
	ax.plot(xr,label = 'X Reference', linewidth = 4)
	box = ax.get_position()
	#Shrink x axis by 20%
	ax.set_position([box.x0, box.y0, box.width *.8, box.height])
	legend = ax.legend(loc = 'center left', bbox_to_anchor = (1,.5))
	plt.show()

camera = GoProHero(password='rafadrone')
camera.command('fov','90')
#camera.command('mode','still')
camera.command('picres','12MP wide')
#camera.command('record','off')

f = open('logfile.txt','w')

lastX = 0
lastY = 0
repeats = 0
xVals = [] 
yVals = []


while repeats < 10:
	frame = getFrame()

	h, w = frame.shape[:2]
	refX = w/2
	refY = h/2 
	ctrs = findTheDot(frame)

	centerX, centerY = findCenter(ctrs)	
	if centerX != -1000:
		controlLaw(centerX, centerY, refX, refY)

		if centerX == lastX:
			repeats = repeats + 1
		else:
			lastX = centerX
			repeats = 0

		if centerY == lastY:
			repeats = repeats + 1
		else:
			lastY = centerY
			repeats = 0
	

	drawAxis(frame)	
	cv2.imshow('frame', frame)
	cv2.waitKey(1)

plotVals(xVals, yVals, w/2, h/2)


