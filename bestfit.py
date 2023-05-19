# -*- coding: utf-8 -*-
"""
Created on Fri May 19 09:17:51 2023

@author: Joshualiu
"""
import time
import numpy as np
from utils import read_instance

num_items, num_bins, weights, capacities = read_instance() 

start_time = time.time()
sol_package = [[] for j in range(num_bins)]
used_cap = [0 for j in range(num_bins)]
'''init i & j'''
i = 0
j = 0
while i < num_items:
    '''get usage'''
    used_bin_cap = used_cap[:(j+1)]
    '''plus the new item'''
    used_cap_with_weight = np.array(used_bin_cap) + weights[i]
    '''empty space'''
    gap_space = np.array(capacities[:(j+1)]) - np.array(used_cap_with_weight)
    
    if sum(gap_space >= 0) > 0:
        adjusted_gap_space = [b if b >=0 else 999 for b in gap_space]
        '''get index of the bin with the maximum load into which the item can fit'''
        k = adjusted_gap_space.index(min(adjusted_gap_space))
        #put item i into the best bin j which can contain it
        sol_package[k].append(i)
        #update the used capacity of bin j
        used_cap[k] += weights[i]   
        i += 1
    else:
        j += 1    

print("--- %s seconds ---" % (time.time() - start_time))
        
for j in range(num_bins):
    if sol_package[j]:
        we = sum(weights[i] for i in sol_package[j])
        print("Bin {} has items {} for a total weight of {}.".format(j, sol_package[j], we))
print("Total {} bin used.".format(sum([1 for j in sol_package if j!=[]])))