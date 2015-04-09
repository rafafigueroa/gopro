#!/usr/bin/env/
from goprohero import GoProHero
import numpy as np
import cv2

camera = GoProHero(password='rafadrone')
#camera.command('record', 'on')
status = camera.status()

pictest = camera.image()

f = open("imagetest.txt","w")
f.write(pictest)
f.close()

#picimg = pictest.decode('base64')
#cv2.imshow('image', picimg)
#try:
#	import cv2
#	from Pillow import Image
#	import StringIO
#	import base64
#except ImportError:
#	pass
	
	
	


