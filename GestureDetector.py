import matplotlib.pyplot as plt
import math
import numpy as np
import nltk

from openpyxl import Workbook, load_workbook
from scipy.ndimage.interpolation import rotate

class GestureDetector:
    
    def translateCoord(self, data, additiveInvers):
        for i in range(0, len(data)):
            # print(data[i][0], additiveInvers[0])
            data[i][0] = data[i][0] + additiveInvers[0]
            data[i][1] = data[i][1] + additiveInvers[1]
            data[i][2] = data[i][2] + additiveInvers[2]
        
        return data
    
    def scaledCoord(self, coords, oldBB, newBB):
        sf = [newBB[0] / oldBB[0], newBB[1] / oldBB[1], newBB[2] / oldBB[2]]
        
        for coord in coords:
            coord[0] *= sf[0]
            coord[1] *= sf[1]
            coord[2] *= sf[2]
        
        return coords
    
    def get3DInfo(self, hand):
        zList = []
        centerPoint = list(hand['center'])
        bbox = hand['bbox']
        
        for item in hand['lmList']:
            zList.append(item[2])
        
        zmin, zmax = min(zList), max(zList)
        
        boxV = zmax - zmin
        bbox = bbox[0], bbox[1], zmin, bbox[2], bbox[3], boxV
        
        cpz = bbox[2] + ((bbox[5]) // 2)
        centerPoint.append(cpz)
        
        return [centerPoint, bbox]
    
    def get_result(self, data):
        categories = data['category'].unique()
        result = {}
        for cat in categories:
            predicted_values = data.loc[data['category']==cat, 'prediction'].to_list()
            frequency_distribution = nltk.FreqDist(predicted_values)
            most_common = frequency_distribution.max()
            result[cat] = most_common
            
        return result
    
    def get_accuracy(self, data, result):
        error = 0
        total_data = data.shape[0]
        for idx, row in data.iterrows():
            ori_values = result[row['category']]
            predicted_values = row['prediction']
            
            if ori_values != predicted_values:
                error += 1
        
        accuracy = ((total_data - error) / total_data) * 100
        
        return accuracy
    
    def rotateCoord(self, coords):
        main_point = coords[0]
        fixedCoord = []
        x, y, z = main_point[0], main_point[1], main_point[2]

        c = math.sqrt(x**2 + y**2)
        tetha = math.degrees(math.asin(abs(y) / c))
        alpha = 90 - tetha
        
        angle = 0
        q = 0
        
        # set quadrant
        if x > 0 and y > 0: q = 1
        elif x < 0 and y > 0: q = 2
        elif x < 0 and y < 0: q = 3
        elif x > 0 and y < 0: q = 4 
        
        # set angle
        if tetha < 30: # rotate horizontally
            if q == 1 or q == 3: 
                angle = -tetha
            elif q == 2 or q == 4:
                angle = tetha
        else: # rotate vertically
            if q == 1 or q == 3:
                angle = alpha
            elif q == 2 or q == 4:
                angle = -alpha
                
        angle = math.radians(angle)
        
        # print('Coordinates: ({}, {}, {})'.format(x, y, z))
        # print('tetha: {}, angle: {}, q: {}'.format(tetha, angle, q))
        
        ry = [
            [math.cos(angle), 0, math.sin(angle)], 
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)]
        ] 
        
        rz = [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ] 
        
        for coord in coords:
            coord = list(np.matmul(rz, coord))
            fixedCoord.append(coord)
        
        # data = np.array(coords)
        # data_rotated = rotate(data, angle=angle)
        # fixedCoord = list(data_rotated)
        # print(fixedCoord)
        
        return fixedCoord
    
    def displayData(self, coords, points):
        x_list = []
        y_list = []
        z_list = []
        
        for coord in coords:
            x_list.append(coord[0])
            y_list.append(coord[1])
            z_list.append(coord[2])
        
        data = [x_list, y_list, z_list]
        data = np.array(data)
        points.set_data(data[0:2, :])
        points.set_3d_properties(data[2, :])
        plt.pause(0.001)
        
    def writeData(self, coord, handType, category, file):
        
        self.wb = load_workbook(file)
        
        # append data into excel for prediction
        data = []
        for item in coord:
            data = [*data, *item]
        
        # append extra data
        binnary_type = 1 if handType == "Right" else 0
        data.append(binnary_type)
        data.append(category)
        
        # append data
        ws = self.wb['Sheet']
        ws.append(data)
        self.wb.save(file)
        
        print('Finish writting {} ...'.format(category))
        