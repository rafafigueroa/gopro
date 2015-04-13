#!/usr/bin/env python

'''
Feature-based image matching sample.

USAGE
  find_obj.py [--feature=<sift|surf|orb>[-flann]] [ <image1> <image2> ]

  --feature  - Feature to use. Can be sift, surf of orb. Append '-flann' to feature name
                to use Flann-based matcher instead bruteforce.

  Press left mouse button on a feature point to see its matching point.
'''

import numpy as np
import cv2
from common import anorm, getsize

FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
FLANN_INDEX_LSH    = 6

def initFindTarget():
	global detector
	global matcher

	detector, matcher = init_feature("sift")
	#detector = cv2.SIFT()
	#matcher = cv2.BFMatcher(cv2.NORM_L2)

def getKPAndDesc(img):
	frameKP, targetDesc = detector.detectAndCompute(img, None)
	return frameKP, targetDesc

def init_feature(name):
    chunks = name.split('-')
    if chunks[0] == 'sift':
        detector = cv2.SIFT()
        norm = cv2.NORM_L2
    elif chunks[0] == 'surf':
        detector = cv2.SURF(800)
        norm = cv2.NORM_L2
    elif chunks[0] == 'orb':
        detector = cv2.ORB(800)
        norm = cv2.NORM_HAMMING
    else:
        return None, None
    if 'flann' in chunks:
        if norm == cv2.NORM_L2:
            flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        else:
            flann_params= dict(algorithm = FLANN_INDEX_LSH,
                               table_number = 6, # 12
                               key_size = 12,     # 20
                               multi_probe_level = 1) #2
        matcher = cv2.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)
    else:
        matcher = cv2.BFMatcher(norm)
    return detector, matcher


def filter_matches(kp1, kp2, matches, ratio = 0.75):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    kp_pairs = zip(mkp1, mkp2)
    return p1, p2, kp_pairs


def findTarget(tKP, tDsc, tImg, fImg):

	fKP, fDsc = detector.detectAndCompute(fImg, None)
	
	print len(fKP)

	h1, w1 = tImg.shape[:2]
	h2, w2 = fImg.shape[:2]
	corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])

	raw_matches = matcher.knnMatch(tDsc, trainDescriptors = fDsc, k = 2) 
	p1, p2, kp_pairs = filter_matches(tKP, fKP, raw_matches)
	if len(p1) > 6:
		H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
		corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2))# + (w1, 0) )
		cenX = int( (corners[0][0] + corners[2][0]) / 2)
		cenY = int( (corners[0][1] + corners[2][1]) / 2)
		maxL = len(p1)
		return True, corners, cenX, cenY 
	else:
		print "Not found!"
		return False, corners, 0, 0 

