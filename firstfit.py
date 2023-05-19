# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:40:48 2023

@author: Joshualiu
"""
import time
from utils import read_instance

num_items, num_bins, weights, capacities = read_instance() 

start_time = time.time()
sol_package = [[] for j in range(num_bins)]
used_cap = [0 for j in range(num_bins)]
'''init j'''
j = 0
for i in range(num_items):
    while j < num_bins:
        if weights[i] <= capacities[j] - used_cap[j]:
            #put item i into the firstbin j which can contain it
            sol_package[j].append(i)
            #update the used capacity of bin j
            used_cap[j] += weights[i]
            break
        else:
            j += 1

print("--- %s seconds ---" % (time.time() - start_time))
        
for j in range(num_bins):
    if sol_package[j]:
        we = sum(weights[i] for i in sol_package[j])
        print("Bin {} has items {} for a total weight of {}.".format(j, sol_package[j], we))
print("Total {} bin used.".format(sum([1 for j in sol_package if j!=[]])))