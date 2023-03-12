# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:19:49 2022

@author: matthew
"""

import cv2
import cvzone
import keyboard
import matplotlib.pyplot as plt

from GestureDetector import GestureDetector
from time import sleep
from openpyxl import Workbook, load_workbook
from cvzone.HandTrackingModule import HandDetector

stdScale = [106, 115, 18] # standard w, h, v
ds = 200 # the axes limit distance from screen
data_file = 'data/Data_AI.xlsx'
cap = cv2.VideoCapture(0)
gestureDetector = GestureDetector()
handDetector = HandDetector(detectionCon=0.8, maxHands=1)

# set graph
fig, ax = plt.subplots()
points, = ax.plot(0, 0, marker='o', linestyle='None')

# set axes limit
ax.set_xlim(-250, 250) 
ax.set_ylim(-250, 250) 
ax.invert_yaxis()

while True:
    _, img = cap.read()
    # img = cv2.flip(img, 1)
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    hands = handDetector.findHands(img, draw=True)
    
    fixedCoord = []
    handType = ''
    
    if hands[0]:
        hand = hands[0][0]
        if hand:
            lmList = hand["lmList"] # list of 21 landmark points
            handType = hand["type"]
            
            handExtraInfo = gestureDetector.get3DInfo(hand) 
            centerPoint = handExtraInfo[0] # cx, cy, cz
            bbox = handExtraInfo[1] # xmin, ymin, zmin, boxW, boxH, boxV
            # fingers = handDetector.fingersUp(hand)
            
            xcp = centerPoint[0]
            ycp = centerPoint[1]
            zcp = centerPoint[2]
            
            # translate to (0, 0, 0)
            additiveInvers = [0-xcp, 0-ycp, 0-zcp]
            fixedCoord = gestureDetector.translateCoord(lmList, additiveInvers)
            fixedCoord = gestureDetector.scaledCoord(fixedCoord, [bbox[3], bbox[4], bbox[5]], stdScale)
            gestureDetector.displayData(fixedCoord, points)
            
    cv2.imshow("Vydsion", img)
    
    # close button is click
    keyCode = cv2.waitKey(1)
    if keyCode > 96 and keyCode < 123:
        if fixedCoord != [] and handType != '':
            gestureDetector.writeData(fixedCoord, handType, chr(keyCode), data_file)
            
    if cv2.getWindowProperty("Vydsion", cv2.WND_PROP_VISIBLE) <1:
        break        
    
cap.release()
cv2.destroyAllWindows()