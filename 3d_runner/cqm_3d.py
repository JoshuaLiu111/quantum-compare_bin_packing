# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:20:12 2023

@author: Joshualiu
"""

from dimod import ConstrainedQuadraticModel,Binary,Real
from dwave.system import LeapHybridCQMSampler
from itertools import permutations
import time
from utils import read_3d
from visualtool import palletplot

def get_indices(name):
    return [int(digs) for digs in name.split('_') if digs.isdigit()]

def cqm_solver(instance:str):

    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance)   

    '''setup formulation'''
    cqm = ConstrainedQuadraticModel()

    #variable
    bin_used = [Binary(f'bin_used_{j}') for j in range(num_bins)]

    item_in_bin = {(i, j): Binary(f'item_{i}_in_bin_{j}')
                   for i in range(num_items) 
                   for j in range(num_bins)}

    x_coord = {i: Real(f'x_{i}',lower_bound=0) for i in range(num_items)}
    y_coord = {i: Real(f'y_{i}',lower_bound=0) for i in range(num_items)}
    z_coord = {i: Real(f'z_{i}',lower_bound=0) for i in range(num_items)}

    rel_x = {(i, ip): Binary(f'{i}_on_right_of_{ip}')
             for i, ip in permutations(range(num_items), r=2)}
    rel_y = {(i, ip): Binary(f'{i}_is_behind_of_{ip}')
             for i, ip in permutations(range(num_items), r=2)}
    rel_z = {(i, ip): Binary(f'{i}_is_above_of_{ip}')
             for i, ip in permutations(range(num_items), r=2)}

    epsilon = 0.01
    Upsilon = 100

    #objective
    cqm.set_objective(sum(bin_used))

    #each item can go into only one bin
    for i in range(num_items):
        cqm.add_constraint(sum(item_in_bin[i,j] for j in range(num_bins)) == 1, label=f'item_placing_{i}')

    #each bin has limited capacity
    for j in range(num_bins):
        cqm.add_constraint(
            sum(weights[i] * item_in_bin[i,j] for i in range(num_items)) - bin_used[j] * capacities[j] <= 0,
            label=f'capacity_bin_{j}')
        
    #items do not exceed their bin size
    for i in range(num_items):
        cqm.add_constraint(x_coord[i] + item_d[i][0] - 
                                    sum(bin_d[j][0]*item_in_bin[i,j] for j in range(num_bins)) <= 0,
                                    label=f'in_length_{i}')
        cqm.add_constraint(y_coord[i] + item_d[i][1] - 
                                    sum(bin_d[j][1]*item_in_bin[i,j] for j in range(num_bins)) <= 0,
                                    label=f'in_width_{i}')
        cqm.add_constraint(z_coord[i] + item_d[i][2] -
                                    sum(bin_d[j][2]*item_in_bin[i,j] for j in range(num_bins)) <= 0,
                                    label=f'in_height_{i}')

    for i, ip in permutations(range(num_items), r=2):
        for j in range(num_bins):
            if i != ip:
                cqm.add_constraint(rel_x[i,ip] + rel_x[ip,i]
                                             + rel_y[i,ip] + rel_y[ip,i]
                                             + rel_z[i,ip] + rel_z[ip,i] -
                                             item_in_bin[i,j] - item_in_bin[ip,j] + 1 >= 0,
                                             label=f'rel_pos_{i}_{ip}_{j}')
        cqm.add_constraint(x_coord[ip] + item_d[ip][0] -
                                   x_coord[i] - (1-rel_x[i,ip])*Upsilon <= 0,
                                   label=f'rel_x_{i}_{ip}')
        cqm.add_constraint(x_coord[i] + epsilon - 
                                    x_coord[ip] - item_d[ip][0] - rel_x[i,ip]*Upsilon <= 0,
                                    label=f'rel_xp_{i}_{ip}')
        cqm.add_constraint(y_coord[ip] + item_d[ip][1] - 
                                   y_coord[i] - (1-rel_y[i,ip])*Upsilon <= 0,
                                   label=f'rel_y_{i}_{ip}')
        cqm.add_constraint(y_coord[i] + epsilon - 
                                    y_coord[ip] - item_d[ip][1] - rel_y[i,ip]*Upsilon <= 0,
                                    label=f'rel_yp_{i}_{ip}')
        cqm.add_constraint(z_coord[ip] + item_d[ip][2] - 
                                   z_coord[i] - (1-rel_z[i,ip])*Upsilon <= 0,
                                   label=f'rel_z_{i}_{ip}')
        
    '''solve the problem'''
    
    sampler = LeapHybridCQMSampler()     

    sampleset = sampler.sample_cqm(cqm,
                                   time_limit=900)
    sampleset.resolve()  
    feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
    if len(feasible_sampleset):      
       best = feasible_sampleset.first

    '''return output'''
    return best.sample.items()


if __name__ == "__main__":
    
    instance = 'input/instance_3d_3.csv'
    start_time = time.time()
    run_results = cqm_solver(instance)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance)
    selected_bins = [key for key, val in run_results if 'bin_used' in key and val]   
    postions = {key:round(val) for key, val in run_results if ('x' in key) | ('y' in key) | ('z' in key)}


    for bi in selected_bins:                        
        in_bin = [key for key, val in run_results if
           "_in_bin" in key and
           get_indices(key)[1] == get_indices(bi)[0]
           and val]
        b = get_indices(in_bin[0])[1]
        sol_pack = [get_indices(item)[0] for item in in_bin]
        sol_pos = [(postions[f'x_{item}'],
                    postions[f'y_{item}'],
                    postions[f'z_{item}']) for item in sol_pack]
        we = sum(weights[i] for i in sol_pack)
        print("Bin {} has items {} for a total weight of {}.".format(b, sol_pack, we))
        
        size_list = []
        bin_size = (bin_d[b][0],bin_d[b][1],bin_d[b][2])
        for i in sol_pack:
            size_list.append((item_d[i][0],item_d[i][1],item_d[i][2]))
        palletplot(bin_size,sol_pos,sol_pack,size_list)
        
    print("Total {} bin used.".format(len(selected_bins)))

