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

HOST = 'edison'
PORT = 50005

edi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
edi.connect((HOST, PORT))

while True:
    print "Sending Secure Message: MHello from Turtlebot 1 to Turtlebot 2!"
    edi.sendall("MHello from Turtlebot 1 to Turtlebot 2!\n")
    time.sleep(5)

	


