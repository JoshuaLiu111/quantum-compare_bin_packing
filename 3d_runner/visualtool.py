#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:57:49 2022

@author: Joshua Liu
"""
# Import all the necessary libraries and packages in the code
import matplotlib.pyplot as plt
import numpy as np
import random


# Defining the user-defined cubes() function
def palletplot(pallet_size:tuple,position_list:list,size_list:list):
    # Defining the size of the axes
    x, y, z = np.indices((10,10,10))
    # Defining the axes and the figure object
    ax = plt.figure(figsize=(9, 9)).add_subplot(projection='3d')
    # Adding pallet size
    axes = [pallet_size[0], pallet_size[1], pallet_size[2]]
    data = np.ones(axes, dtype=np.bool)
    # Transparency
    alpha = 0.3
    colors = np.empty(axes + [4], dtype=np.float32)
    colors[:] = [1, 0, 0, alpha]
    ax.voxels(data, facecolors=colors)
    # Adding boxes
    for i in range(len(position_list)):
        # Defining the length of the sides of the box
        cube = (position_list[i][0] <= x) & (x < (size_list[i][0] + position_list[i][0])) & \
               (position_list[i][1] <= y) & (y < (size_list[i][1] + position_list[i][1])) & \
               (position_list[i][2] <= z) & (z < (size_list[i][2] + position_list[i][2]))
        # Defining the colors for the box
        colors = np.empty(cube.shape, dtype=object)
        # Random colors
        colors[cube] = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])      
        # Plotting the box in the figure
        ax.voxels(cube, facecolors=colors)
    # Displaying the graph
    plt.show()
