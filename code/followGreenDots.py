from __future__ import division
#import base64
import numpy as np
import cv2
import cv
from PIL import Image
import StringIO
#from goprohero import GoProHero
import time
import os
import matplotlib.pyplot as plt
import socket

HOST = '10.1.1.128'
PORT = 50017

cmdCount = 0
	
def drawAxis(aframe):

	#h = 480
	#w = 640
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
	M = cv2.getRotationMatrix2D(center, 90, 1.0)
	rotated = cv2.warpAffine(img, M, (w,h))
	return rotated

def controlLaw( x,y, refx, refy ):

	global cmdCount
	global s
	k = .15 
	spd = -k * (  refx - x )
	
	print "X:",x,"  Ref:",refx, "   Speed:",spd

	cmdCount = cmdCount + 1
	s.sendall(str(spd))
	xVals.append(x)
	yVals.append(y)
	logStr = "X Actual: " + str(x) + "X Reference: " + str(refx) + "\n"
	f.write(logStr)

def getFrame():
	_,img = cap.read();
	rotframe = rotate90(img)
	
	return rotframe


def findTheDot(theframe):
	greenF = frame[:,:,1]	
	#imgray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
	#Threshold the green channel (use HSV later...)	
	_, thresh = cv2.threshold(greenF, 250, 255, cv2.THRESH_BINARY)
	
	# Clean up the image a bit before looking for contours...
	kernel = np.ones((2,2),np.uint8)
	img1 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
	cleanImage = cv2.morphologyEx(img1, cv2.MORPH_CLOSE, kernel)
	
	
	ctrs, hier = cv2.findContours(cleanImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(cleanImage, ctrs, -1, (255, 255, 255), 3)
	cv2.imshow('Cleaned',cleanImage)
	cv2.imshow('Threshed', thresh)
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

def drawTrackingCircle(frame, cX, cY):
	cv2.circle(frame, (cX, cY), 10, [255,255,255], 4)

cap = cv2.VideoCapture(1)

#fgbg = cv2.BackgroundSubtractorMOG()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
f = open('logfile.txt','w')

lastX = 0
lastY = 0
repeats = 0
xVals = [] 
yVals = []


while True:
	frame = getFrame()

	#fgMask = fgbg.apply(frame)
	#cv2.imshow('fg mask', fgMask)
	#masked = cv2.bitwise_and(frame, frame, mask = fgMask)
	#cv2.imshow('result', masked)


	h, w = frame.shape[:2]
	refX = 290 #w/2
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
	drawTrackingCircle(frame, centerX, centerY)
	cv2.imshow('frame', frame)
	ch = cv2.waitKey(1)
	if ch == 'q':
		break

plotVals(xVals, yVals, w/2, h/2)


