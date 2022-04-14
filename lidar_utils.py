import sys
import os
import time

import numpy as np
import math
import statistics as sts
import matplotlib.pyplot as plt

## adds the fsds package located the parent directory to the pyhthon path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import fsds

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(abs(x1-x2), 2) + math.pow(abs(y1-y2), 2))

def vectDistance(v1,v2):
    return math.sqrt((v1[0]-v2[0])**2+(v1[1]-v2[1])**2)

def vectAverage(v1,v2):
    vx = 0.5*(v1[0]+v2[0])
    vy = 0.5*(v1[1]+v2[1])
    return np.array([vx,vy])

def pointgroup_to_cone(group):
    average_x = 0
    average_y = 0
    for point in group:
        average_x += point[0]
        average_y += point[1]
    average_x = average_x / len(group)
    average_y = average_y / len(group)
    return([average_x, average_y])
    #return ([-1*average_y, average_x])

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(abs(x1-x2), 2) + math.pow(abs(y1-y2), 2))

def rotate(point, angle):

    px, py = point[:, 0], point[:, 1]
    rotated = np.empty((point.shape[0], 2))
    rotated[:, 0] = math.cos(angle) * px - math.sin(angle) * py
    rotated[:, 1] = math.sin(angle) * px + math.cos(angle) * py
    return rotated

def anglefilter(fsds_or):
    z_or = fsds_or
    z_orneg=False
    if z_or<0:
        z_orneg=True
    z_angle = 2*math.asin(z_or)*180/math.pi
    if z_orneg==True:
        z_angle += 360
    return z_angle

def EstimateConeColor(relCones):
    colorVector = np.empty((0,1))
    for rrCones in relCones:
        print (rrCones)
        if -rrCones[1] < 0:
            colorVector = np.r_[colorVector,[[0]]]
        else:
            colorVector = np.r_[colorVector,[[4]]]
    relCones = np.c_[relCones,colorVector]
    
    return relCones

def ColorVector(relCones):
    colorVector = np.empty((0,1))
    for rrCones in relCones:
        print (rrCones)
        if -rrCones[1] < 0:
            colorVector = np.r_[colorVector,[[0]]]
        else:
            colorVector = np.r_[colorVector,[[4]]]
    return colorVector

def ColorVector1(relCones):
    colorVector = np.empty((0,1))
    for rrCones in relCones:
        if -rrCones[1] < 0:
            distance_score = (-1)/(distance(0,0,rrCones[0],rrCones[1]))
            colorVector = np.r_[colorVector,[[distance_score]]]
        else:
            distance_score = (+1)/(distance(0,0,rrCones[0],rrCones[1]))
            colorVector = np.r_[colorVector,[[distance_score]]]
    return colorVector

def plotEachSweep0(relCones,plotLimit):
    plt.pause(0.1)
    plt.clf()
    plt.axis([-plotLimit, plotLimit, -2, plotLimit])
    plt.scatter(-relCones[:,1],relCones[:,0], color='blue')
    plt.scatter(0,0,color='red')

def plotEachSweep1(relCones,plotLimit):
    plt.pause(0.1)
    plt.clf()
    rotated_relCones = EstimateConeColor(relCones)
    print('---')
    print(rotated_relCones)
    colors = np.where(np.where(rotated_relCones[:,-1] == 4, "y", rotated_relCones[:,-1]) == "0.0", "b", np.where(rotated_relCones[:,-1] == 4, "y", rotated_relCones[:,-1]))
    plt.axis([-plotLimit, plotLimit, -2, plotLimit])
    plt.scatter(-relCones[:,1],relCones[:,0], color=colors)
    plt.plot()

def plotEachSweepGlobal(globCones,globCar,color_vector):
    plt.pause(0.5)
    plt.clf()
    #colors = np.where(color_vector[:,-1] > 0,"y","b")
    #colors = np.where(np.where(color_vector[:,-1] > 0, "y", color_vector[:,-1]) == "-1.0", "b", np.where(color_vector[:,-1] > 0, "y", color_vector[:,-1]))
    colors = np.where(np.where(color_vector[:,-1] == 4, "y", color_vector[:,-1]) == "0.0", "b", np.where(color_vector[:,-1] == 4, "y", color_vector[:,-1]))
    print(colors)
    plt.scatter(globCones[:,0],globCones[:,1],c=colors)
    plt.scatter(globCar[:,0],globCar[:,1],c='red')

def globalPlot(gCones,carPos,color_vector):
    plt.pause(0.1)
    plt.clf()
    plt.scatter(gCones[:,0],gCones[:,1])
    plt.scatter(carPos[0],carPos[1],c='red')
              
## AutoControls
def calculate_steering(cones,max_steering):
    average_y = 0
    for cone in cones:
        average_y += cone
    average_y = average_y / len(cones)

    if average_y > 0:
        print('left || Average: {}'.format(average_y))
        return -max_steering
        
    else:
        print('right || Average: {}'.format(average_y))
        return max_steering

    
def calculate_throttle(gps,max_throttle,target_speed):

    velocity = math.sqrt(math.pow(gps.gnss.velocity.x_val, 2) + math.pow(gps.gnss.velocity.y_val, 2))

    return max_throttle * max(1 - velocity / target_speed, 0)
