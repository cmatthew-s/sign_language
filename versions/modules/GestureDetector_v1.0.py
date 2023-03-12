import matplotlib.pyplot as plt

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
    
    def displayData(self, coords, points):
        x_list = []
        y_list = []
        
        for coord in coords:
            x_list.append(coord[0])
            y_list.append(coord[1])
            
        points.set_data(x_list, y_list)
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
        