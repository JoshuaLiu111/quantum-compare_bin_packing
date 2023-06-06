# -*- coding: utf-8 -*-
"""
Created on Mon May 22 11:38:55 2023

@author: Joshualiu
"""

import time
import numpy as np
from utils import read_3d
from visualtool import palletplot
from animationtool import aniplot

'''prepare'''
def rank_list(lst:list) -> list:
    ranked_indices = sorted(range(len(lst)), key=lambda i: lst[i])
    return ranked_indices

def bf_solver(instance:str) -> list:
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance)
    
    sol_package = [[] for j in range(num_bins)]
    sol_pacposition = [[] for j in range(num_bins)]
    used_cap = [0 for j in range(num_bins)]
    ep_list = [[(0, 0, 0)] for j in range(num_bins)]
    
    '''rank by size'''
    sorted_item_list = sorted(range(num_items), 
                              key=lambda i: (np.prod(item_d[i]),
                                             item_d[i][0],
                                             item_d[i][1]), reverse=True)
    '''init i & j'''
    i = 0
    j = 0
    while i < num_items:
        '''get usage'''
        used_bin_cap = used_cap[:(j + 1)]
        '''plus the new item'''
        used_cap_with_weight = np.array(used_bin_cap) + weights[sorted_item_list[i]]
        '''empty space'''
        gap_space = np.array(capacities[:(j + 1)]) - np.array(used_cap_with_weight)
        '''number of possible bins'''
        poss_bin = sum(gap_space >= 0)

        if poss_bin > 0:
            adjusted_gap_space = [b if b >= 0 else 999 for b in gap_space]
            '''get index of the bin with the maximum load into which the item can fit'''
            ranked_list = rank_list(adjusted_gap_space)[:poss_bin]
            indicator = False
            for k in ranked_list:
                # 3d capacity
                eps = sorted(ep_list[k], key=lambda ep: (ep[0], ep[1], ep[2]))
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
                    # no overlap & no exceed
                    if (
                        ep[0] + item_d[sorted_item_list[i]][0] <= bin_d[k][0]
                        and ep[2] + item_d[sorted_item_list[i]][2] <= bin_d[k][2]
                        and ep[1] + item_d[sorted_item_list[i]][1] <= bin_d[k][1]
                        and not size_condition
                    ):
                        indicator = True
                        # record position
                        sol_pacposition[k].append(ep)
                        # clean eps
                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[k].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[k].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2])) < 1:
                            ep_list[k].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2]))
                        else:
                            ep_list[k].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2]))

                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2])) < 1:
                            ep_list[k].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))
                        else:
                            ep_list[k].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))

                        if eps.count((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[k].append((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[k].remove((ep[0] + item_d[sorted_item_list[i]][0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[k].append((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[k].remove((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0], ep[1], ep[2] + item_d[sorted_item_list[i]][2])) < 1:
                            ep_list[k].append((ep[0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))
                        else:
                            ep_list[k].remove((ep[0], ep[1], ep[2] + item_d[sorted_item_list[i]][2]))

                        if eps.count((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2])) < 1:
                            ep_list[k].append((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))
                        else:
                            ep_list[k].remove((ep[0], ep[1] + item_d[sorted_item_list[i]][1], ep[2]))

                        ep_list[k].remove(ep)
                        # record packing
                        sol_package[k].append(sorted_item_list[i])
                        # update the used capacity of bin j
                        used_cap[k] += weights[sorted_item_list[i]]
                        break
                if indicator:
                    break
            if indicator:
                # next
                i += 1
            else:
                j += 1
        else:
            j += 1
    
    return [sol_package,sol_pacposition]


if __name__ == "__main__":
    
    instance = 'input/instance_3d_3.csv'
    instance_code = int(instance.split('_')[-1].split('.')[0])
    start_time = time.time()
    sol_package,sol_pacposition = bf_solver(instance)
    print("--- %s seconds ---" % (time.time() - start_time))
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance)
        
    for j in range(num_bins):
        if sol_package[j]:
            we = sum(weights[i] for i in sol_package[j])
            print("Bin {} has items {} for a total weight of {}.".format(j, sol_package[j], we))
            
            bin_size = (bin_d[j][0],bin_d[j][1],bin_d[j][2])
            size_list = [(item_d[i][0],item_d[i][1],item_d[i][2]) for i in sol_package[j]]
            palletplot(bin_size,sol_pacposition[j],sol_package[j],size_list)
            aniplot(bin_size,sol_pacposition[j],sol_package[j],size_list,
                    f'output/bf_wr_ins_{instance_code}_bin_{j}.mp4')

    print("Total {} bin used.".format(sum([1 for j in sol_package if j!=[]])))    