# Finds the countours by looking for the brightes object in the green frame.
import cv2

def getContours(theframe):
        greenF = theframe[:,:,1]
        #imgray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(greenF, 254, 255, cv2.THRESH_BINARY)
	_, threshR = cv2.threshold(theframe[:,:,2], 240, 255, cv2.THRESH_BINARY)

        ctrs, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(thresh, ctrs, -1, (255, 255, 255), 3)
	cv2.imshow('red', threshR)
        cv2.imshow('green', greenF)
        cv2.imshow('threshold',thresh)
        return ctrs

