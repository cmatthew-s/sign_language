# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:19:49 2022

@author: matthew
"""

import cv2
import cvzone
import keyboard
import itertools
import pandas as pd
import pickle
import numpy as np
import nltk
import json

from GestureDetector import GestureDetector
from time import sleep
from joblib import load
from openpyxl import Workbook, load_workbook
from cvzone.HandTrackingModule import HandDetector
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# define variables
coords = []
index = 0
offset = 20

# define parameters
stdScale = [106, 115, 18] # standard w, h, v
ds = 200 # the axes limit distance from screen
data_file = 'data/Data_AI.xlsx'
cap = cv2.VideoCapture(0)
gestureDetector = GestureDetector()
handDetector = HandDetector(detectionCon=0.8, maxHands=1)

# load models
scaler = StandardScaler()
pca = PCA(n_components=10)
kmeans = pickle.load(open('./model/kmeans.pkl', 'rb'))

with open('./data/result.txt') as fp:
    result = json.load(fp)

while True:
    _, img = cap.read()
    # img = cv2.flip(img, 1)
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    hands = handDetector.findHands(img, draw=False)

    fixedCoord = []
    handType = ''
    
    prediction = ''
    x, y, w, h = 0, 0, 0, 0

    if hands:
        hand = hands[0]
        if hand:
            lmList = hand["lmList"] # list of 21 landmark points
            handType = hand["type"]
            x,y,w,h = hand['bbox']
            
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
            
            # predict data
            data = list(itertools.chain.from_iterable(fixedCoord))
            coords.append(data)
            
            if len(coords) > 14:
                pred_data = coords[index:len(coords)]
                pred_data = np.array(pred_data)
                data_scaled = scaler.fit_transform(pred_data.T).T
                cat = kmeans.predict(data_scaled)[-1] 
                
                for key in result.keys():
                    values_result = result[key]
                    if cat == values_result:
                        prediction = key
                    
                index+=1 
    
    if (x > 0 and y > 0 and w > 0 and h > 0):
        # cv2.rectangle(img,(x-offset,y-offset-50),(x-offset+90,y-offset-50+50),(255,0,255),cv2.FILLED)
        cv2.putText(img, prediction, (x-15,y-52), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255,255,255),2, cv2.LINE_AA)
        cv2.rectangle(img,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,255,255),2)
        
    cv2.imshow("Vydsion", img)
    
    # close button is click
    keyCode = cv2.waitKey(1)
    if cv2.getWindowProperty("Vydsion", cv2.WND_PROP_VISIBLE) <1:
        break        
    
cap.release()
cv2.destroyAllWindows()