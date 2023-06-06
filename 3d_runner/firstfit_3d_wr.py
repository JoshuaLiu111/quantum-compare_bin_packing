# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:44:55 2023

@author: Joshualiu
"""

import time
import numpy as np
from utils import read_3d
from visualtool import palletplot

def ff_solver(instance:str) -> list:
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance)

    sol_package = [[] for j in range(num_bins)]
    sol_pacposition = [[] for j in range(num_bins)]
    used_cap = [0 for j in range(num_bins)]
    ep_list = [[(0,0,0)] for j in range(num_bins)]
    '''rank by size'''
    sorted_item_list = sorted(range(num_items), 
                              key=lambda i: (np.prod(item_d[i]),
                                             item_d[i][0],
                                             item_d[i][1]), reverse=True)
    '''init j'''
    j = 0

    for i in range(num_items):
        while j < num_bins:
            indicator = False
            #Check pallet capacity
            if weights[sorted_item_list[i]] <= capacities[j] - used_cap[j]:
                #3d capacity
                eps = sorted(ep_list[j], key=lambda ep: (ep[0], ep[1], ep[2]))
                for ep in eps:
                    size_condition = False
                    for ep2 in eps:
                        if ep2 != ep:
                            if ep[1] == ep2[1] and ep[2] == ep2[2]:
                                if ep[0] + item_d[sorted_item_list[i]][0] > ep2[0]:
                                    size_condition = True
                                    break
                            elif ep[0] == ep2[0] and ep[2] == ep2[2]:
                                if ep[1] + item_d[sorted_item_list[i]][1] > ep2[1]:
                                    size_condition = True
                                    break
                    #no overlap & no exceed
                    if ep[0] + item_d[sorted_item_list[i]][0] <= bin_d[j][0] and \
                        ep[2] + item_d[sorted_item_list[i]][2] <= bin_d[j][2] and \
                         ep[1] + item_d[sorted_item_list[i]][1] <= bin_d[j][1] and not size_condition:
                        indicator = True
                        #record position
                        sol_pacposition[j].append(ep)
                        #clean eps
                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[j].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[j].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2])) < 1:
                            ep_list[j].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2]))
                        else:
                            ep_list[j].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2]))

                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2])) < 1:
                            ep_list[j].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))
                        else:
                            ep_list[j].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))

                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[j].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[j].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[j].append((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[j].remove((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0], ep[1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[j].append((ep[0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[j].remove((ep[0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2])) < 1:
                            ep_list[j].append((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))
                        else:
                            ep_list[j].remove((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))

                        ep_list[j].remove(ep)
                        #record packing
                        sol_package[j].append(sorted_item_list[i])
                        #update the used capacity of bin j
                        used_cap[j] += weights[sorted_item_list[i]]
                        break
            if indicator == True:
                break
            else:
                j += 1 
    
    return [sol_package,sol_pacposition]


if __name__ == "__main__":
    
    instance = 'input/instance_3d_3.csv'
    start_time = time.time()
    sol_package,sol_pacposition = ff_solver(instance)
    print("--- %s seconds ---" % (time.time() - start_time))
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance)
        
    for j in range(num_bins):
        if sol_package[j]:
            we = sum(weights[i] for i in sol_package[j])
            print("Bin {} has items {} for a total weight of {}.".format(j, sol_package[j], we))
        
            bin_size = (bin_d[j][0],bin_d[j][1],bin_d[j][2])
            size_list = [(item_d[i][0],item_d[i][1],item_d[i][2]) for i in sol_package[j]]
            palletplot(bin_size,sol_pacposition[j],sol_package[j],size_list)

    print("Total {} bin used.".format(sum([1 for j in sol_package if j!=[]])))


    