import sys
import os
import time

import numpy as np
import math
import matplotlib.pyplot as plt

from lidar_utils import *
from lidar_clustering import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import fsds

cones_range_cutoff = 5

# connect to the simulator 
client = fsds.FSDSClient()

# Check network connection, exit if not connected
client.confirmConnection()

def raw_Lidar():
    lidardata = client.getLidarData(lidar_name = 'Lidar1')
    point_cloud = lidardata.point_cloud
    if len(point_cloud) < 3:
        return np.array([[0, 0 ,0]])
    points = np.array(point_cloud, dtype=np.dtype('f4'))
    return np.reshape(points, (int(points.shape[0]/3), 3))


while True:
    cones = raw_Lidar()
    plt.pause(1)
    print(cones)
    plt.clf()
    print(cones.shape)
    x = np.array(cones[:,0])
    y = np.array(cones[:,1])

    plt.scatter(-y,x)
   
