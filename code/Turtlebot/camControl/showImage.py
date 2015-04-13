import cv2

cap = cv2.VideoCapture(1)
ret,img = cap.read()
cv2.imshow("blah", img)
cv2.waitKey(0)
