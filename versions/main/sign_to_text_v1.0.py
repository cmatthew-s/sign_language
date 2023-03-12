# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:19:49 2022

@author: matthew
"""

import cv2
import cvzone
import keyboard

from time import sleep
from openpyxl import Workbook, load_workbook
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
handDetector = HandDetector(detectionCon=0.8, maxHands=1)
data_file = '../data/Data_AI.xlsx'

wb = load_workbook(data_file)

def translateCoord(data, additiveInvers):
    # translate coordinates with the additive invers
    for i in range(0, len(data)):
        # print(data[i][0], additiveInvers[0])
        data[i][0] = data[i][0] + additiveInvers[0]
        data[i][1] = data[i][1] + additiveInvers[1]
        data[i][2] = data[i][2] + additiveInvers[2]
    
    return data

def write_data(coord, handType, category, wb=wb):
    # append data into excel for prediction
    data = []
    for item in coord:
        data = [*data, *item]
    
    # append extra data
    binnary_type = 1 if handType == "Right" else 0
    data.append(binnary_type)
    data.append(category)
    
    # append data
    ws = wb['Sheet']
    ws.append(data)
    wb.save('Data_AI.xlsx')
    
    print('Finish writting {} ...'.format(category))
    
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
            fixedCoord = translateCoord(lmList, additiveInvers)
            
    cv2.imshow("Vydsion", img)
    
    # close button is click
    keyCode = cv2.waitKey(1)
    if keyCode > 96 and keyCode < 123:
        if fixedCoord != [] and handType != '':
            write_data(fixedCoord, handType, chr(keyCode))
            
    if cv2.getWindowProperty("Vydsion", cv2.WND_PROP_VISIBLE) <1:
        break        
    
cap.release()
cv2.destroyAllWindows()