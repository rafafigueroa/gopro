import base64
import numpy as np
import cv2
import cv
from PIL import Image
import StringIO
from goprohero import GoProHero
import time
import os


def getFrame():
	imgstr = camera.image()[21:];	
	imgraw = base64.decodestring(imgstr)
	pilImage = Image.open(StringIO.StringIO(imgraw));
	frame = np.array(pilImage)
	return frame

def findTheDot(theframe):	
	imgray=cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
	greenF = theframe[:,:,1]
	ret, thresh = cv2.threshold(greenF, 240, 255, cv2.THRESH_BINARY)
	cv2.imshow("thresh", thresh)
	img1 = thresh.copy()
	contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(img1, contours, -1, (255, 255, 255), 5)
	cv2.imshow("Cont", img1)
	cv2.waitKey(1)
	return contours


camera = GoProHero(password='rafadrone')
camera.command('fov','90')
#camera.command('mode','still')
camera.command('picres','12MP wide')
#camera.command('record','off')

cntX = 0
while True:
	frame = getFrame()
	redF = frame[:,:,2]
	cv2.imshow('frame', frame)
	#blueF = frame[:,:,0]
	#greenF = frame[:,:,1]
	redF = frame[:,:,2]
	cv2.waitKey(1)

	ctrs0 = findTheDot(frame)	

	
		#cv2.drawContours( redF, ctrs0, -1, (128, 255,255), 3)
	#binc = cv2.cvtColor(binf, cv2.COLOR_GRAY2BGR)
	#cv2.line(binc,(cnX,cnY),(cnX+50,cnY),[0,0,255],thickness = 4)
	#cv2.line(binc,(cnX,cnY),(cnX, cnY-50),[255,0,0],thickness = 4) 
		#cv2.imshow('Dot', redF)

	#cv2.line(frame, (cnX, cnY),(cnX+50,cnY), [0, 0, 255],thickness = 4)
	#cv2.line(frame, (cnX, cnY),(cnX, cnY-50),[255,0,0], thickness = 4)
	#cv2.line(bwc, (cnX, cnY),(cnX+50,cnY), [0, 0, 255],thickness = 4)
	#cv2.line(bwc, (cnX, cnY),(cnX, cnY-50),[255,0,0], thickness = 4)
	#cv2.imshow('bw',bwc)
	
	cv2.waitKey(1)
	
