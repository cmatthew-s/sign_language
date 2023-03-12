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
fig = plt.figure()
ax = plt.axes(projection='3d')
points, = ax.plot3D(0, 0, 0, marker='o', linestyle='None')

# set axes options
ax.set_xlim(-150, 150) 
ax.set_ylim(-150, 150) 
ax.set_zlim(-35, 35)
ax.invert_yaxis()
ax.view_init(280, 90)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

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
            fixedCoord = gestureDetector.rotateCoord(fixedCoord)
            gestureDetector.displayData(fixedCoord, points)
            
    cv2.imshow("Vydsion", img)
    
    # close button is click
    keyCode = cv2.waitKey(1)
    if keyCode > 96 and keyCode < 123:
        if fixedCoord != [] and handType != '':
            gestureDetector.writeData(fixedCoord, handType, chr(keyCode), data_file)
    if keyCode == 63:
        if fixedCoord != [] and handType != '':
            customCategory = input('Input your categories here: ')
            gestureDetector.writeData(fixedCoord, handType, customCategory, data_file)
    # elif keyCode == 32:
    #     if fixedCoord != [] and handType != '':
    #         angle = gestureDetector.rotateCoord(fixedCoord)
            
    if cv2.getWindowProperty("Vydsion", cv2.WND_PROP_VISIBLE) <1:
        break        
    
cap.release()
cv2.destroyAllWindows()