# -*- coding: utf-8 -*-
"""
Created on Fri May 12 10:30:53 2023

@author: Joshualiu
"""

from dimod import ConstrainedQuadraticModel,Binary
from dwave.system import LeapHybridCQMSampler
import time
from utils import read_instance

num_items, num_bins, weights, capacities = read_instance()    

'''setup formulation'''
cqm = ConstrainedQuadraticModel()

#objective
bin_used = [Binary(f'bin_used_{j}') for j in range(num_bins)]
cqm.set_objective(sum(bin_used))

#each item can go into only one bin
item_in_bin = [[Binary(f'item_{i}_in_bin_{j}') for j in range(num_bins)] 
               for i in range(num_items)]
for i in range(num_items):
    one_bin_per_item = cqm.add_constraint(sum(item_in_bin[i]) == 1, label=f'item_placing_{i}')

#each bin has limited capacity
for j in range(num_bins):
    bin_up_to_capacity = cqm.add_constraint(
        sum(weights[i] * item_in_bin[i][j] for i in range(num_items)) - bin_used[j] * capacities[j] <= 0,
        label=f'capacity_bin_{j}')

'''solve the problem'''
start_time = time.time()
sampler = LeapHybridCQMSampler()     

sampleset = sampler.sample_cqm(cqm,
                               time_limit=20,
                               label="SDK Examples - 1D Bin Packing")
sampleset.resolve()  
feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
if len(feasible_sampleset):      
   best = feasible_sampleset.first

'''return output'''

print("--- %s seconds ---" % (time.time() - start_time))

selected_bins = [key for key, val in best.sample.items() if 'bin_used' in key and val]   

def get_indices(name):
    return [int(digs) for digs in name.split('_') if digs.isdigit()]

for bin in selected_bins:                        
    in_bin = [key for key, val in best.sample.items() if
       "_in_bin" in key and
       get_indices(key)[1] == get_indices(bin)[0]
       and val]
    b = get_indices(in_bin[0])[1]
    w = [get_indices(item)[0] for item in in_bin]
    we = sum(weights[i] for i in w)
    print("Bin {} has items {} for a total weight of {}.".format(b, w, we))
    
print("Total {} bin used.".format(len(selected_bins)))
