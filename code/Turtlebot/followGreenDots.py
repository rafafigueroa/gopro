from __future__ import division
import numpy as np
import cv2
import cv
from PIL import Image
import StringIO
import time
import os
import matplotlib.pyplot as plt
import socket

from blobDetect import getContours 
import findTarget

HOST = '10.1.1.128'
PORT = 50007

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

def motorTurn(degrees):
	global edi 

	if degrees < 0:
		degrees = -degrees
		mOnDelay = int((degrees / 400) * 1000.0) 
		if mOnDelay > 999:
			mOnDelay = 999
		cmdString = "{:+4},{:+4},{:3}".format(int(-30),0,int(mOnDelay))
	else:
		mOnDelay = int((degrees / 400) * 1000.0) 
		if mOnDelay > 999:
			mOnDelay = 999
		cmdString = "{:+4},{:+4},{:3}".format(int(30),0,int(mOnDelay))

	print "Rotating " + str(degrees) + " by " + str(mOnDelay) + "mSecs"

	edi.sendall(cmdString)
	cv2.waitKey(50)

def controlLaw( x,y, refx, refy ):

	global cmdCount
	global edi 
	k = .15 
	spd = -k * (  refx - x )
	
	print "X:",x,"  Ref:",refx, "   Speed:",spd

	cmdCount = cmdCount + 1
	cmdString = "{:+4},{:+4},{:3}".format(int(spd), 0, 35)
	print "Cmd String: " + cmdString
	edi.sendall(cmdString)
	xVals.append(x)
	yVals.append(y)
	logStr = "X Actual: " + str(x) + "X Reference: " + str(refx) + "\n"
	#f.write(logStr)
	#time.sleep(.003) #Give Edison time to issue motor commands

def getFrame():
	_,img = cap.read();
	_,img = cap.read();
	_,img = cap.read();
	rotframe = rotate90(img)
	bwframe = cv2.cvtColor(rotframe, cv2.COLOR_BGR2GRAY)
	return rotframe, bwframe

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

def initTarget2():
	findTarget.initFindTarget()
	img = []
	target = []

	imgBase = cv2.imread("n2Front.jpg",cv2.IMREAD_GRAYSCALE)
	kpB, dB = findTarget.getKPAndDesc( imgBase )
	
	return kpB, dB, imgBase

def coerceToRange(val, minV, maxV):
	if val < minV:
		return minV
	if val > maxV:
		return maxV
	return val

def centerTarget( kpB, dB, imgB, cX, cY):
	print "Found, centering..."
	h = 320
	w = 640
	rX = w/2
	rY = h/2

	while abs(cX - rX) > 60:
		mv = cX - rX
		if mv < 0:
			motorTurn( -15 )
		else:
			motorTurn( 15 )
		frame, bwframe = getFrame()
		found, corners, centerX, centerY = findTarget.findTarget(kpB, dB, imgB, bwframe)
		if found == False:
			print "Lost Target!"
			return False
	return True

	
		
cap = cv2.VideoCapture(1)
edi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
edi.connect((HOST, PORT))
#f = open('logfile.txt','w')

lastX = 0
lastY = 0
repeats = 0
xVals = [] 
yVals = []

kpB, dB, imgB = initTarget2()
ROIx1 = 0
ROIx2 = 480
ROIy1 = 0
ROIy2 = 640
while True:
	frame,bwframe = getFrame()
	h, w = frame.shape[:2]
	refX = 310 #w/2
	refY = h/2

	#First try to find the target in the frame...

	#roiFrame = bwframe[ ROIy1:ROIy2, ROIx1:ROIx2]
	#cv2.imshow("ROI", roiFrame)

	found, corners, centerX, centerY = findTarget.findTarget(kpB, dB, imgB, bwframe)
	if found == True:
		#cv2.polylines(frame,[corners], True, (255,255,255))
		#The target has been located.
		#Try to center the target
		if centerTarget(kpB, dB, imgB, centerX, centerY) == True:
			#Fine control.
			print "Fine control!"
			print "Stopping..."
			exit()
	else: 
		print "Looking for target..."
		motorTurn(25)
		



	#	centerX = centerX + ROIx1
	#	centerY = centerY + ROIy1
	#	print "Corners:"
	#	print corners
	#	print "Center:"
	#	print centerX, centerY
	
		#ROIx1 = corners[0][0] - 25
		#ROIy1 = corners[0][1] - 25
		#ROIx2 = corners[2][0] + 25
		#ROIy2 = corners[2][1] + 25
	#	print "Next ROI:[" + str(ROIx1) + "," + str(ROIy1) + "],[" + str(ROIx2) + "," + str(ROIy2)+ "]"
		#ROIx1 = coerceToRange(ROIx1, 0, w)
		#ROIx2 = coerceToRange(ROIx2, 0, w)
		#ROIy1 = coerceToRange(ROIy1, 0, h)
		#ROIy2 = coerceToRange(ROIy2, 0, h)
	#	print corners
	
		#cv2.polylines(frame, [corners], True, (255, 255, 255))	
		#drawTrackingCircle(frame, centerX, centerY)
		#controlLaw(centerX, centerY, refX, refY)

	drawAxis(frame)	
	cv2.imshow('frame', frame)
	cv2.waitKey(10)

plotVals(xVals, yVals, w/2, h/2)


