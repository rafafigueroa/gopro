from __future__ import division
import numpy as np
import cv2
import time
import os
import matplotlib.pyplot as plt
import socket
import math

from blobDetect import getContours 
import findTarget

HOST = 'Edison'
PORT = 50005

cmdCount = 0

def setExposure(exposure):
        #print "Setting Exposure to " + str(exposure)
        setExp = "camControl/setExposure " + str(exposure)
        os.system(setExp)

	
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
	M = cv2.getRotationMatrix2D(center, 90, 1.0)
	rotated = cv2.warpAffine(img, M, (w,h))
	return rotated

def motorTurn():
    global edi 

    cmdString = "{:+4},{:+4},{:3}\n".format(int(-30),0,int(150))
    #edi.sendall(cmdString)
    cv2.waitKey(50)

def controlLaw( x,y, refx, refy ):

    global cmdCount
    global edi 
    k = .25

    spd = -k * (  refx - x )

    print "X:",x,"Y: ",y,"  Ref:",refx, "   Speed:",spd

    cmdCount = cmdCount + 1
    cmdString = "{:+4},{:+4},{:3}\n".format(int(spd), 0, 35)
    print "Cmd String: " + cmdString
    #edi.sendall(cmdString)
    xVals.append(x)
    yVals.append(y)
    logStr = "X Actual: " + str(x) + "X Reference: " + str(refx) + "\n"
    #f.write(logStr)
    time.sleep(.025) #Give Edison time to issue motor commands

def getFrame(cap, skip):

    setExposure(200)
    for i in range(skip):
        _,img2 = cap.read()
    setExposure(160)
    for i in range(skip):
        _,img = cap.read()
    _, img = cap.read()
    workframe = rotate90(img)
    visframe  = rotate90(img2)

    return workframe, visframe 

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

def coerceToRange(val, minV, maxV):
	if val < minV:
		return minV
	if val > maxV:
		return maxV
	return val

def lineProperties(centers):

    x = centers[1][0] - centers[0][0]
    y = centers[0][1] - centers[1][1]

    print "x: " + str(x) + "  y:" + str(y)
    llen = math.sqrt(x**2 + y**2)
    if (llen == 0):
        return 0,0,0
    ang = math.asin(y/llen)
    print "Angle: " + str(ang) + " Length:" + str(llen)
    print "Inches to Pixels:" + str(llen / .75)
    return ang, llen, llen / .75

def locateTarget(cap):

    spotted = 0
    notSpotted = 0
    pi = math.pi

    while (spotted < 3):
        img, vis = getFrame(cap, 15)
        contours = findTarget.findTarget(img)
        centers = findTarget.findCentroids(contours)
        if len(centers) == 2:
            ang, llen,_ = lineProperties(centers)
            print "Possible Target sighted!"
            if abs(ang) > .600 and abs(ang) < 1.00:
               print "Angle within limits..."
               spotted = spotted + 1
               notSpotted = 0
            else:
                print "Rejected:" + str(ang)
                notSpotted = notSpotted + 1
                spotted = 0
        else:
            print "Target not sighted!"
            spotted = 0
            notSpotted = notSpotted + 1
        if notSpotted >= 3:
            print "Looking elsewhere..."
            motorTurn()
            notSpotted = 0
            spotted = 0

def calibration(cap):

    calibrationX = 1
    _, vis = getFrame(cap, 5)
    cv2.imshow("Calibration", vis)
    while True:
        print "Align, press a key..."
        cv2.waitKey(0)
        img, vis = getFrame(cap, 15)
        cv2.imshow("Calibration", vis)
        contours = findTarget.findTarget(img)
        centers = findTarget.findCentroids(contours)
             
        if len(centers) == 2:	
            _,_,cvt = lineProperties(centers)
            cX = (centers[0][0] + centers[1][0]) / 2
            cY = (centers[0][1] + centers[1][1]) / 2

            

            print "Old: " + str(calibrationX) + " Error: " + str(320 - (calibrationX * cvt) - cX)
            calibrationX = (320 - cX) / cvt
            print "New Calibration: " + str(calibrationX) + "  New Error: " + str( 320 - (calibrationX * cvt) - cX)



def alignLaser(cap):

    print "Aligning Laser"
    cX = 0
    refX = 290 
    refY = 192 
    notDone = False
    aligned = 0
    while aligned < 3:
        if (abs(cX - refX) < 3 ): 
            aligned = aligned + 1
        else:
            aligned = 0
        img, vis = getFrame(cap, 15)	
        contours = findTarget.findTarget(img)
        centers = findTarget.findCentroids(contours)
        if len(centers) == 1:
            print "One dot!"
            cX = centers[0][0]
            cY = centers[0][1]
            drawTrackingCircle(img, int(cX), int(cY))
            cv2.imshow("frame", img)
            cv2.waitKey(1)
            controlLaw(cX, cY, refX, refY)
        if len(centers) == 2:	
            _,_,cvt = lineProperties(centers)
            cX = (centers[0][0] + centers[1][0]) / 2
            cY = (centers[0][1] + centers[1][1]) / 2 
    
            #refX = int( 320 - (calibrationX * cvt ))
            #refY = int( cY - ( 3.3 * cvt) ) 


            drawTrackingCircle(vis,int(cX),int(cY))
            #drawTrackingCircle(vis,refX, refY) 
            drawAxis(vis)
            cv2.imshow("frame", vis)
            cv2.waitKey(1)
            controlLaw(cX, cY, refX, refY)
        else:
            print "Not enough centers:" + str(centers)
            
		
cap = cv2.VideoCapture(1)
edi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
edi.connect((HOST, PORT))
#f = open('logfile.txt','w')

lastX = 0
lastY = 0
repeats = 0
xVals = [] 
yVals = []
calibrationX = 1.7 # Inches from center

#calibration(cap)
setExposure(200)
#    h, w = frame.shape[:2]
refX = 310 #w/2
    #refY = h/2

locateTarget(cap)
print "Target found! Aligning laser!"

alignLaser(cap)
    #First try to find the target in the frame...

print "Finished!"
cv2.waitKey(0)

plotVals(xVals, yVals, w/2, h/2)


