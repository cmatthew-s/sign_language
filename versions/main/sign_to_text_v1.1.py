# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:19:49 2022

@author: matthew
"""

import cv2
import cvzone
import keyboard
from GestureDetector import GestureDetector

from time import sleep
from openpyxl import Workbook, load_workbook
from cvzone.HandTrackingModule import HandDetector

data_file = 'data/Data_AI.xlsx'
cap = cv2.VideoCapture(0)
gestureDetector = GestureDetector()
handDetector = HandDetector(detectionCon=0.8, maxHands=1)
    
while True:
    _, img = cap.read()
    # img = cv2.flip(img, 1)
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    hands = handDetector.findHands(img, draw=True)
    
    # get the screen center
    (h, w) = img.shape[:2]
    screenCenter = [w/2, h/2]
    xsc = screenCenter[0]
    ysc = screenCenter[1]
    
    fixedCoord = []
    handType = ''
    
    if hands[0]:
        hand = hands[0][0]
        if hand:
            lmList = hand["lmList"] # list of 21 landmark points
            centerPoint = hand["center"] # center point of the hand cx, cy
            handType = hand["type"]
            fingers = handDetector.fingersUp(hand)
            
            xcp = centerPoint[0]
            ycp = centerPoint[1]
            # xcp = lmList[8][0]
            # ycp = lmList[8][1]
            zcp = lmList[8][2] # the index finger tip z coord
            
            # z coord will be normalize to 0
            additiveInvers = [xsc-xcp, ysc-ycp, 0 - zcp]
            fixedCoord = gestureDetector.translateCoord(lmList, additiveInvers)
            
    cv2.imshow("Vydsion", img)
    
    # close button is click
    keyCode = cv2.waitKey(1)
    if keyCode > 96 and keyCode < 123:
        if fixedCoord != [] and handType != '':
            gestureDetector.write_data(fixedCoord, handType, chr(keyCode), data_file)
            
    if cv2.getWindowProperty("Vydsion", cv2.WND_PROP_VISIBLE) <1:
        break        
    
cap.release()
cv2.destroyAllWindows()