# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:26:13 2023

@author: Joshualiu
"""

import numpy as np
import csv
import re

'''random parameters'''
def random_gen() -> dict:
    '''set para'''
    num_items = 75
    num_bins = 45
    item_weight_range = [3, 8]
    bin_capacity_range = [10,15]
    weights = list(np.random.randint(*item_weight_range, num_items))
    capacities = list(np.random.randint(*bin_capacity_range, num_bins))
    
    return {'num_items':num_items, 
            'num_bins':num_bins, 
            'item_weights':weights, 
            'capacities':capacities}

def read_instance(data_path:str = "data/instance_1.csv") -> list:
    with open(data_path, 'r') as file:
        csvreader = csv.reader(file)
        '''git rid of quotation'''
        clean_list = [[re.findall(r"[-+]?(?:\d*\.*\d+)",e) for e in row[1:]] for row in csvreader]
        clean_list = [[float(ep[0]) for ep in e] for e in clean_list]
        clean_list = [int(e[0]) if len(e) == 1 else e for e in clean_list]
        return clean_list

if __name__ == "__main__":
    '''random data'''
    instance = random_gen()
    '''write to csv'''
    with open('data/instance_1.csv', 'w') as f:
        for key in instance.keys():
            f.write("%s,%s\n"%(key,instance[key]))