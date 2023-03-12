# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:19:49 2022

@author: matthew
"""

import cv2
import cvzone

from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
handDetector = HandDetector(detectionCon=0.8, maxHands=1)
   
def print_formated_coord(data):
    for item in data:
        print(item)
        
while True:
    _, img = cap.read()
    # img = cv2.flip(img, 1)
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    hands = handDetector.findHands(img, draw=True)
    
    fixedCoord = []
    if hands[0]:
        hand = hands[0][0]
        if hand:
            fixedCoord = hand["lmList"] # list of 21 landmark points
            
    cv2.imshow("Vydsion", img)
    
    # close button is click
    keyCode = cv2.waitKey(1)
    if keyCode > 96 and keyCode < 123:
        if fixedCoord != []:
            print_formated_coord(fixedCoord)
            
    if cv2.getWindowProperty("Vydsion", cv2.WND_PROP_VISIBLE) <1:
        break        
    
cap.release()
cv2.destroyAllWindows()