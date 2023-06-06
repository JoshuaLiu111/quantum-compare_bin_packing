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
from matplotlib import gridspec

# Defining the user-defined cubes() function
def palletplot(pallet_size: tuple, position_list: list, item_list: list, size_list: list):
    # Defining the size of the axes
    x, y, z = np.indices((10, 10, 10))
    # Defining the axes and the figure object
    fig = plt.figure(figsize=(9, 9))
    gs = gridspec.GridSpec(1, 2, width_ratios=[6, 1], wspace=0.1)
    ax = fig.add_subplot(gs[0], projection='3d')
    legend_ax = fig.add_subplot(gs[1])

    # Adding pallet size
    axes = [pallet_size[0], pallet_size[1], pallet_size[2]]
    data = np.ones(axes, dtype=bool)
    # Transparency
    alpha = 0.3
    colors = np.empty(axes + [4], dtype=np.float32)
    colors[:] = [1, 0, 0, alpha]
    ax.voxels(data, facecolors=colors)

    # Adding boxes
    legend_patches = []
    for i in range(len(position_list)):
        # Defining the length of the sides of the box
        cube = (position_list[i][0] <= x) & (x < (size_list[i][0] + position_list[i][0])) & \
               (position_list[i][1] <= y) & (y < (size_list[i][1] + position_list[i][1])) & \
               (position_list[i][2] <= z) & (z < (size_list[i][2] + position_list[i][2]))
        # Defining the colors for the box
        colors = np.empty(cube.shape, dtype=object)
        # Random colors
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])
        colors[cube] = color
        # Plotting the box in the figure
        ax.voxels(cube, facecolors=colors)
        legend_patches.append((color, f'item_{item_list[i]}'))

    # Plotting colored patches with box numbers in the legend
    for i, (color, label) in enumerate(legend_patches):
        legend_ax.add_patch(plt.Rectangle((0, i), 1, 1, facecolor=color, edgecolor='none'))
        legend_ax.text(1.2, i+0.5, label, va='center', fontsize=15)
    legend_ax.set_xlim([0, 2])
    legend_ax.set_ylim([0, len(legend_patches)])
    legend_ax.axis('off')

    # Adjusting subplot margins and spacing
    ax.margins(0.01)
    legend_ax.margins(0.01)
    gs.tight_layout(fig, rect=[0, 0, 1, 1])

    # Displaying the graph
    plt.show()


if __name__ == "__main__":
    '''test'''
    art_bin_size = [6, 7, 7]
    art_pos = [(0, 0, 0), (0, 0, 3), (0, 3, 0),
               (0, 3, 3), (3, 0, 0), (3, 0, 3),
               (3, 0, 5), (3, 3, 0), (3, 3, 2),
               (3, 3, 4)]
    art_list = list(range(10))
    art_size = [(3, 3, 3), (3, 3, 3), (3, 3, 3),
                (3, 3, 3), (3, 3, 3), (3, 3, 2),
                (3, 3, 2), (3, 3, 2), (3, 3, 2),
                (3, 3, 2)]
    #static
    palletplot(art_bin_size,art_pos,art_list,art_size)
    
