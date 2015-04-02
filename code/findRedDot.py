import cv2
import numpy as np

frame = cv2.imread('image.png')
cv2.imshow('test', frame)

bw = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(bw, 219, 255, cv2.THRESH_BINARY)
cv2.imshow('mask', mask)
cv2.waitKey(0)


