"""
README
To use this code, follow the step below :
Tools > Preferences > IPython Console > Graphics > Backend

Set the value to Qt5
"""

import matplotlib.pyplot as plt 
import numpy as np

fig, ax = plt.subplots()

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]

for t in range(10):
    if t == 0:
        points, = ax.plot(x, y, marker='o', linestyle='None')
        ax.set_xlim(-300, 300) 
        ax.set_ylim(-300, 300) 
    else:
        new_x = np.random.randint(10, size=5)
        new_y = np.random.randint(10, size=5)
        points.set_data(new_x, new_y)
    
    plt.pause(0.5)