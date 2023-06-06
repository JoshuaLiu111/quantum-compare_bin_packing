# -*- coding: utf-8 -*-
"""
Created on Thu May 25 18:48:13 2023

@author: Joshualiu
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


def aniplot(pallet_size: tuple, position_list: list, item_list: list, size_list: list, out_path: str):
    # Generate a color list
    color_list = ["#"+''.join([random.choice('ABCDEF0123456789') for _ in range(6)]) for _ in range(100)]
    # Defining the size of the axes
    x, y, z = np.indices((10, 10, 10))
    # Defining the axes and the figure object
    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(1, 2, width_ratios=[6, 1], wspace=0.1)

    ax = fig.add_subplot(gs[0, 0], projection='3d')
    legend_ax = fig.add_subplot(gs[0, 1])

    def update(frame):
        ax.cla()  # Clear the main plot
        # Adding pallet size
        axes = [pallet_size[0], pallet_size[1], pallet_size[2]]
        data = np.ones(axes, dtype=bool)
        # Transparency
        alpha = 0.3
        colors = np.empty(axes + [4], dtype=np.float32)
        colors[:] = [1, 0, 0, alpha]
        ax.voxels(data, facecolors=colors)
        # Adding boxes up to the current frame
        for i in range(frame + 1):
            # Defining the length of the sides of the box
            cube = (position_list[i][0] <= x) & (x < (size_list[i][0] + position_list[i][0])) & \
                   (position_list[i][1] <= y) & (y < (size_list[i][1] + position_list[i][1])) & \
                   (position_list[i][2] <= z) & (z < (size_list[i][2] + position_list[i][2]))
            # Defining the colors for the box
            colors = np.empty(cube.shape, dtype=object)
            # Random colors
            colors[cube] = color_list[i]
            # Plotting the box in the figure
            ax.voxels(cube, facecolors=colors)

        # Update the legend
        legend_ax.cla()  # Clear the legend plot
        legend_patches = []
        for i in range(len(position_list)):
            legend_patches.append((color_list[i], f'item_{item_list[i]}'))
        for i, (color, label) in enumerate(legend_patches):
            legend_ax.add_patch(plt.Rectangle((0, i), 1, 1, facecolor=color, edgecolor='none'))
            legend_ax.text(1.2, i+0.5, label, va='center', fontsize=15)
        legend_ax.set_xlim([0, 2])
        legend_ax.set_ylim([0, len(legend_patches)])
        legend_ax.axis('off')

    # Create the animation
    frames = len(position_list)
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=1000, blit=False)

    ani.save(out_path, fps=2, extra_args=['-vcodec', 'libx264'])
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
    out_path = 'output/trial.mp4'
    #animation
    aniplot(art_bin_size,art_pos,art_list,art_size,out_path)