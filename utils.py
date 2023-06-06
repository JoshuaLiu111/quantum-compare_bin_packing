# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:26:13 2023

@author: Joshualiu
"""

import numpy as np
import csv
import re

'''random 1d'''
def random_gen(num_items:int, num_bins:int) -> dict:
    '''set para'''
    item_weight_range = [3, 6]
    bin_capacity_range = [80,100]
    weights = list(np.random.randint(*item_weight_range, num_items))
    capacities = list(np.random.randint(*bin_capacity_range, num_bins))
    
    return {'num_items':num_items, 
            'item_weights':weights, 
            'num_bins':num_bins, 
            'capacities':capacities}

def write_instance(instance:dict, data_path:str):
    '''write to csv'''
    with open(data_path, 'w') as f:
        for key in instance.keys():
            f.write("%s,%s\n"%(key,instance[key]))

def read_instance(data_path:str) -> list:
    with open(data_path, 'r') as file:
        csvreader = csv.reader(file)
        '''git rid of quotation'''
        clean_list = [[re.findall(r"[-+]?(?:\d*\.*\d+)",e) for e in row[1:]] for row in csvreader]
        clean_list = [[int(ep[0]) for ep in e] for e in clean_list]
        clean_list = [e[0] if len(e) == 1 else e for e in clean_list]
        return clean_list

'''random 3d'''
def random_3d(num_items:int, num_bins:int) -> dict:
    '''set para'''
    item_weight_range = [3,6]
    bin_capacity_range = [80,100]
    item_dimension_range = [2,4]
    bin_dimension_range = [7,10]
    weights = list(np.random.randint(*item_weight_range, num_items))
    capacities = list(np.random.randint(*bin_capacity_range, num_bins))
    item_d = np.array_split(np.random.randint(*item_dimension_range, 3*num_items), num_items)
    bin_d = np.array_split(np.random.randint(*bin_dimension_range, 3*num_bins), num_bins)
    
    return {'num_items':num_items, 
            'item_weights':weights, 
            'item_dimensions':item_d,
            'num_bins':num_bins, 
            'capacities':capacities,
            'bin_dimensions':bin_d}

def read_3d(data_path:str) -> list:
    with open(data_path, 'r') as file:
        csvreader = csv.reader(file)
        '''git rid of quotation'''
        clean_list = [[re.findall(r"[-+]?(?:\d*\.*\d+)",e) for e in row[1:]] for row in csvreader]
        clean_list = [[int(ep[0]) for ep in e] for e in clean_list]
        clean_list = [e[0] if len(e) == 1 else e for e in clean_list]
        '''break dimensions'''
        clean_list[2] = np.array_split(clean_list[2],clean_list[0])
        clean_list[5] = np.array_split(clean_list[5],clean_list[3])
        return clean_list
    
    
if __name__ == "__main__":
    '''random data'''
    instance = random_3d(200,20)
    '''write'''
    write_instance(instance,'3d_runner/input/instance_3d_3.csv')