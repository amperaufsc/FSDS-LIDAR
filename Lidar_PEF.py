import sys
import os
import time

import numpy as np
import math
import matplotlib.pyplot as plt

import keyboard

from lidar_utils import *

## adds the fsds package located the parent directory to the pyhthon path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import fsds


# connect to the simulator 
client = fsds.FSDSClient()

# Check network connection, exit if not connected
client.confirmConnection()

plotLimit = 7 # m

def lidarSweep():
    lidardata = client.getLidarData(lidar_name = 'Lidar1')
    point_cloud = lidardata.point_cloud
    if len(point_cloud) < 3:
        return np.array([[0, 0 ,0]])
    points = np.array(point_cloud, dtype=np.dtype('f4'))
    return np.reshape(points, (int(points.shape[0]/3), 3))

def Main():
    globCones = list()
    globCar = list()
    while True:
        pointCloud = lidarSweep()

        cones = onlyCones(pointCloud,plotLimit)
        relCones = np.array(cones)
        if len(cones) == 0:
            continue

        print('======================')
        print(relCones)

        time.sleep(0.3)
        plotEachSweep(relCones,plotLimit) #Plota imagem relativa de uma varredura

        if keyboard.is_pressed('q') == True: ##Definição de parada
            break

if __name__ == '__main__':
    Main()