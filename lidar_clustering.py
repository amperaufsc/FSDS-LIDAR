import sys
import os
import time

import numpy as np
import math
import statistics as sts
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

from lidar_utils import *

def firstClustering(points,plotLimit):
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

def CustomShape(cone,plotLimit):
    ## custom shape type = parabola.
    x = -cone[1]
    y = cone[0]
    if (y+4*x+20>0) and (y-4*x+20>0) and (y>0) and (y<plotLimit):
        return True
    else:
        return False


def firstClustering_CustomShape(points,plotLimit):
    current_group = []
    cones = []
    for i in range(1, len(points)):

        distance_to_last_point = distance(points[i][0], points[i][1], points[i-1][0], points[i-1][1])

        if distance_to_last_point < 0.1:
            current_group.append([points[i][0], points[i][1]])
        else:
            if len(current_group) > 0:
                cone = pointgroup_to_cone(current_group)
                # if distance(0, 0, cone[0], cone[1]) < plotLimit:
                #     cones.append(cone)
                if CustomShape(cone,plotLimit) == True:
                    cones.append(cone)
                current_group = []
    return cones

def AbsoluteClustering(cones,cone_colors):
    tree = cKDTree(cones)
    rows_to_fuse = np.array(list(tree.query_pairs(r=0.5)))
    delete_col = list()
    for rtf in rows_to_fuse:
        x,y = vectAverage(cones[rtf[0]],cones[rtf[1]])
        np.put(cones,2*rtf[0],x)
        np.put(cones,2*rtf[0]+1,y)
        delete_col.append(rtf[1])
    cones = np.delete(cones,delete_col,axis=0)
    cone_colors = np.delete(cone_colors,delete_col,axis=0)
    cones = np.c_[cones,cone_colors]
    return cones

def AbsoluteClustering1(cones,cone_colors):
    tree = cKDTree(cones)
    rows_to_fuse = np.array(list(tree.query_pairs(r=0.5)))
    delete_col = list()
    for rtf in rows_to_fuse:
        x,y = vectAverage(cones[rtf[0]],cones[rtf[1]])
        color_score = cone_colors[rtf[0]] + cone_colors[rtf[1]]
        np.put(cones,2*rtf[0],x)
        np.put(cones,2*rtf[0]+1,y)
        np.put(cone_colors,rtf[0],color_score)
        delete_col.append(rtf[1])
    cones = np.delete(cones,delete_col,axis=0)
    cone_colors = np.delete(cone_colors,delete_col,axis=0)
    cone_colors = np.where(cone_colors < 0,0,4)
    cones = np.c_[cones,cone_colors]
    return cones

def GroupClustering(cones,cone_colors):
    tree = cKDTree(cones)
    rows_to_fuse = np.array(list(tree.query_pairs(r=0.5)))
    delete_col = list()
    for rtf in rows_to_fuse:
        x,y = vectAverage(cones[rtf[0]],cones[rtf[1]])
        color_score = cone_colors[rtf[0]+rtf[1]]

        np.put(cones,2*rtf[0],x)
        np.put(cones,2*rtf[0]+1,y)
        
        np.put(cone_colors,rtf[0],color_score)
        delete_col.append(rtf[1])
    cones = np.delete(cones,delete_col,axis=0)
    cone_colors = np.delete(cone_colors,delete_col,axis=0)
    return cones

def SecondClustering(currentCones,groupCones): #####NAO USAR
    for cCones in currentCones:
        for gCones in groupCones:
            gCones = np.array(gCones)
            if vectDistance(cCones,gCones) < 0.5:
                groupCones = np.where(groupCones==gCones,vectAverage(cCones,gCones),groupCones)
            else:
                groupCones = np.r_[groupCones,[cCones]]
    groupCones = np.unique(groupCones,axis=0)
    return groupCones