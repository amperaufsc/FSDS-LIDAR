import sys
import os
import time

import numpy as np
import math
import matplotlib.pyplot as plt

## adds the fsds package located the parent directory to the pyhthon path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import fsds

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(abs(x1-x2), 2) + math.pow(abs(y1-y2), 2))

def pointgroup_to_cone(group):
    average_x = 0
    average_y = 0
    for point in group:
        average_x += point[0]
        average_y += point[1]
    average_x = average_x / len(group)
    average_y = average_y / len(group)
    return ([-1*average_y, average_x])

def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(abs(x1-x2), 2) + math.pow(abs(y1-y2), 2))

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def anglefilter(fsds_or):
    z_or = fsds_or
    z_orneg=False
    if z_or<0:
        z_orneg=True
    z_angle = 2*math.asin(z_or)*180/math.pi
    if z_orneg==True:
        z_angle += 360
    return z_angle

def plotEachSweep(relCones,plotLimit):
    plt.pause(0.1)
    plt.clf()
    plt.axis([-plotLimit, plotLimit, -2, plotLimit])
    plt.scatter(relCones[:,0],relCones[:,1])


def onlyCones(points,plotLimit):
    current_group = []
    cones = []
    for i in range(1, len(points)):

        distance_to_last_point = distance(points[i][0], points[i][1], points[i-1][0], points[i-1][1])

        if distance_to_last_point < 0.1:
            current_group.append([points[i][0], points[i][1]])
        else:
            if len(current_group) > 0:
                cone = pointgroup_to_cone(current_group)
                if distance(0, 0, cone[0], cone[1]) < plotLimit:
                    cones.append(cone)
                current_group = []
    return cones

