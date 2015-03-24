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
camera.command('record','on')

#imgstr = open("testimage.txt","rb").read()
cv.NamedWindow('display1')
cv.MoveWindow('display1',10, 10)

while True:
	imgstr = camera.image()[21:]	
#	open("test.txt","w").write(imgstr).close()
	imgraw = base64.decodestring(imgstr)
	pilImage = Image.open(StringIO.StringIO(imgraw));
	npImage = np.array(pilImage)
	#matImage = cv.fromarray(npImage)
	cv2.imshow('display1', npImage)
	print("Waiting for a key...")
	cv2.waitKey(1)
	print("Getting next image...")
	
	#time.sleep(1)
