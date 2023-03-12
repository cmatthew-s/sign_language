import matplotlib.pyplot as plt
import math
import numpy as np

from openpyxl import Workbook, load_workbook

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
    
    def rotateCoord(self, coords):
        main_point = coords[0]
        c1 = math.sqrt(main_point[0]**2 + main_point[1]**2)
        tetha = math.degrees(math.asin(abs(main_point[1]) / c1))
        alpha = 90 - tetha
        
        angle_y = 0
        fixedCoord = []
        
        if main_point[0] > 0 and main_point[1] > 0:
            angle_y = self.decideCoords(main_point[0], main_point[1], tetha, alpha, 1)
            
        elif main_point[0] < 0 and main_point[1] > 0:
            angle_y = self.decideCoords(main_point[0], main_point[1], tetha, alpha, 2)
                
        elif main_point[0] < 0 and main_point[1] < 0:
            angle_y = self.decideCoords(main_point[0], main_point[1], tetha, alpha, 3)
                
        else:
            angle_y = self.decideCoords(main_point[0], main_point[1], tetha, alpha, 4)
        
        ry = [
            [math.cos(angle_y), 0, math.sin(angle_y)], 
            [0, 1, 0],
            [-math.sin(angle_y), 0, math.cos(angle_y)]
        ]
        
        rz = [
            [math.cos(angle_y), -math.sin(angle_y), 0],
            [math.sin(angle_y), math.cos(angle_y), 0],
            [0, 0, 1]
        ]
        
        for coord in coords:
            coord = list(np.matmul(rz, coord))
            fixedCoord.append(coord)
            
        return fixedCoord
    
    def decideCoords(self, x, y, tetha, alpha, q):
        if abs(x)**2 < abs(y)**2:
            if q == 1 or q == 3:
                # print('KW I and KW III')
                return alpha
            elif q == 2 or q == 4:
                # print('KW II and KW IV')
                return -alpha
        else:
            if q == 1 or q == 3:
                # print('KW I and KW III')
                return -tetha
            elif q == 2 or q == 4:
                # print('KW II and KW IV')
                return tetha
    
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
        