# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys

cap = cv2.VideoCapture(0)
#set the width and height, and UNSUCCESSFULLY set the exposure time
cap.set(3,1080)
cap.set(4,1024)
cap.set(15, 0.1)
flag, frame = cap.read()
width = np.size(frame, 1)
height = np.size(frame, 0)

def corner(filename) : 
 im= filename

 gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

 corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
 corners = np.int0(corners)

 for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,(0,0,255),-1)
 return im

while True:
    ret, img = cap.read()
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
    x = width/2
    y = height/2
    text_color = (255,0,0)
    cv2.putText(img, "your_string", (x,y), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=1)
    cv2.imshow("input",corner(img))
    #cv2.imshow("thresholded", imgray*thresh2)

    key = cv2.waitKey(10)
    if key == 27:
        break


cv2.destroyAllWindows() 
cv2.VideoCapture(0).release()