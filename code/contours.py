from __future__ import division
import numpy as np
import cv2


if __name__ == '__main__':
    #img = make_image()
    img1 = cv2.imread('image.png')
    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img2, 220, 255, cv2.THRESH_BINARY)
    h, w = img.shape

    ctrs0, hier = cv2.findContours( img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]
   
 
    vis = np.zeros((h, w, 3), np.uint8)
    cv2.drawContours( vis, ctrs0, -1, (128,255,255), 3)
    M = cv2.moments(ctrs0[0])
    cntX = int(M['m10']/M['m00'])
    cntY = int(M['m01']/M['m00'])
    cv2.line(vis, (cntX, cntY),(int(w/2), int(h/2)), [255,0,0])
    cv2.imshow('contours', vis)
    cv2.imshow('image', img)
    cv2.waitKey()
