# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:44:55 2023

@author: Joshualiu
"""

import time
import numpy as np
from utils import read_3d
from visualtool import palletplot
from animationtool import aniplot

def ff_solver(instance:str) -> list:
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance)

    sol_package = [[] for _ in range(num_bins)]
    sol_pacposition = [[] for _ in range(num_bins)]
    used_cap = [0 for _ in range(num_bins)]
    #extreme points
    ep_list = [[(0,0,0)] for _ in range(num_bins)]
    #restart points
    rp_list = [[(0,0,0)] for _ in range(num_bins)]
    # Rank by size
    sorted_item_list = sorted(range(num_items), 
                              key=lambda i: (np.prod(item_d[i]),
                                             item_d[i][0],
                                             item_d[i][1]), reverse=True)

    j = 0

    for i in range(num_items):
        while j < num_bins:
            indicator = False
            # Check pallet capacity
            if weights[sorted_item_list[i]] <= capacities[j] - used_cap[j]:
                # 3D capacity
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
                    # No overlap & no exceed
                    if (ep[0] + item_d[sorted_item_list[i]][0] <= bin_d[j][0] and
                        ep[2] + item_d[sorted_item_list[i]][2] <= bin_d[j][2] and
                        ep[1] + item_d[sorted_item_list[i]][1] <= bin_d[j][1] and
                        not size_condition):
                        indicator = True
                        
                        # Record position
                        sol_pacposition[j].append(ep)

                        # Clean eps
                        new_ep = (ep[0] + item_d[sorted_item_list[i]][0],
                                  ep[1] + item_d[sorted_item_list[i]][1],
                                  ep[2] + item_d[sorted_item_list[i]][2])
                        if eps.count(new_ep) < 1:
                            ep_list[j].append(new_ep)
                        else:
                            ep_list[j].remove(new_ep)

                        new_ep = (ep[0] + item_d[sorted_item_list[i]][0],
                                  ep[1],
                                  ep[2])
                        if eps.count(new_ep) < 1:
                            ep_list[j].append(new_ep)
                        else:
                            ep_list[j].remove(new_ep)

                        new_ep = (ep[0] + item_d[sorted_item_list[i]][0],
                                  ep[1] + item_d[sorted_item_list[i]][1],
                                  ep[2])
                        if eps.count(new_ep) < 1:
                            ep_list[j].append(new_ep)
                        else:
                            ep_list[j].remove(new_ep)

                        new_ep = (ep[0] + item_d[sorted_item_list[i]][0],
                                  ep[1],
                                  ep[2] + item_d[sorted_item_list[i]][2])
                        if eps.count(new_ep) < 1:
                            ep_list[j].append(new_ep)
                        else:
                            ep_list[j].remove(new_ep)

                        new_ep = (ep[0],
                                  ep[1] + item_d[sorted_item_list[i]][1],
                                  ep[2] + item_d[sorted_item_list[i]][2])
                        if eps.count(new_ep) < 1:
                            ep_list[j].append(new_ep)
                        else:
                            ep_list[j].remove(new_ep)

                        new_ep = (ep[0],
                                  ep[1],
                                  ep[2] + item_d[sorted_item_list[i]][2])
                        if eps.count(new_ep) < 1:
                            ep_list[j].append(new_ep)
                        else:
                            ep_list[j].remove(new_ep)

                        new_ep = (ep[0],
                                  ep[1] + item_d[sorted_item_list[i]][1],
                                  ep[2])
                        if eps.count(new_ep) < 1:
                            ep_list[j].append(new_ep)
                        else:
                            ep_list[j].remove(new_ep)

                        ep_list[j].remove(ep)
                        # Record packing
                        sol_package[j].append(sorted_item_list[i])
                        # Update the used capacity of bin j
                        used_cap[j] += weights[sorted_item_list[i]]
                        break

                # Refresh ep list
                if not indicator and len(ep_list[j]) != 1:
                    #clean ep_list
                    map_list = [(point[0],point[1]) for point in ep_list[j] if point[2] != 0]
                    
                    occurrences = {}
                    for item in map_list:
                        if item in occurrences:
                            occurrences[item] += 1
                        else:
                            occurrences[item] = 1
                    margin_point = [item for item in map_list if occurrences[item] == 1]
                    #artificial points - make sure not the previous start point
                    art_list = [(point[0],point[1],0) for point in margin_point
                                if point[0] != rp_list[j][-1][0] or point[1] != rp_list[j][-1][1]]
                    #get empty space
                    inverse_dems = [bin_d[j] - point for point in art_list]
                    inverse_volumns = [dem[0]*dem[1]*dem[2] for dem in inverse_dems]
                    edge_point = art_list[inverse_volumns.index(max(inverse_volumns))]
                    #update ep_list and rp_list
                    ep_list[j] = [edge_point]
                    rp_list[j].append(edge_point)
                    
                    j -= 1
                        
            if indicator:
                break
            else:
                j += 1

    return [sol_package, sol_pacposition]


if __name__ == "__main__":
    
    instance = 'input/instance_3d_3.csv'
    instance_code = int(instance.split('_')[-1].split('.')[0])
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
            aniplot(bin_size,sol_pacposition[j],sol_package[j],size_list,
                    f'output/ff_wr_ins_{instance_code}_bin_{j}.mp4')

    print("Total {} bin used.".format(sum([1 for j in sol_package if j!=[]])))


    