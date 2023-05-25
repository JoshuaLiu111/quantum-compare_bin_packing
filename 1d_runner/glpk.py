# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:59:49 2023

@author: Joshualiu
"""
import pyomo.environ as pyo
from typing import Dict, Any
import time
from utils import read_instance

num_items, weights, num_bins, capacities = read_instance("input/instance_1.csv") 

# Initialise data_dict
def data_reader() -> dict:
    
    data_dict: Dict[str, Dict[Any, Any]] = {}

    # Sets
    data_dict["I"] = {
        None: [i for i in range(num_items)]
    }
    data_dict["J"] = {
        None: [j for j in range(num_bins)]
    }

    #Paras
    data_dict["w"] = {
        i : weights[i] for i in range(num_items)
    }
    data_dict["v"] = {
        j : capacities[j] for j in range(num_bins)
    }
    return data_dict

data = {None: data_reader()}

'''setup formulation'''
def define_model() -> pyo.AbstractModel:
    
    model = pyo.AbstractModel()

    '''variables'''
    # Set of items
    model.I = pyo.Set()
    # Set of bins
    model.J = pyo.Set()

    # weight of box
    model.w = pyo.Param(model.I)
    # capacity of bin
    model.v = pyo.Param(model.J)

    # if box i is in bin j
    model.p = pyo.Var(model.I*model.J, within=pyo.Boolean)
    # if bin j is used
    model.u = pyo.Var(model.J, within=pyo.Boolean)

    # objective:minimize the number of bin used
    def total_number(model):
        return (sum(model.u[j] for j in model.J))
    model.total = pyo.Objective(rule=total_number, sense=pyo.minimize)

    # constraint:each item is allocated to exactly one bin:
    def assign(model, i):
        return sum(model.p[i,j] for j in model.J) == 1
    model.assignment = pyo.Constraint(model.I, rule=assign)

    # constraint:maximum capacity of each bin j cannot be exceeded:
    def cap(model, j):
        return sum(model.w[i]*model.p[i,j] for i in model.I) <= model.v[j]*model.u[j]
    model.capacity = pyo.Constraint(model.J, rule=cap)

    return model

def write_vars(instance: pyo.ConcreteModel):
    """Writes decision variables to list of dicts."""

    var_outputs = [
        {"variable": v.name, "index": index, "value": pyo.value(v[index])}
        for v in instance.component_objects(pyo.Var, active=True)
        for index in v
    ]
    
    return var_outputs

def cal_solution_cost(instance:pyo.AbstractModel):
    """Calculates total cost of entities"""
    sol_total_cost =  sum(pyo.value(instance.u[j]) for j in instance.J) 
    return sol_total_cost

'''run the formulation'''
abstract_model = define_model()
instance = abstract_model.create_instance(data)

opt = pyo.SolverFactory("glpk")

opt.options["tmlim"] = 100
opt.options["mipgap"] = 0.00001

start_time = time.time()

opt.solve(instance, tee=True)

print("--- %s seconds ---" % (time.time() - start_time))

var_outputs = write_vars(instance)
cost = cal_solution_cost(instance)

b = [v['value'] for v in var_outputs if v['variable'] == 'u']
w = [[] for j in b]

for v in var_outputs:
    if v['variable'] == 'p' and v['value'] == 1:
        w[v['index'][1]].append(v['index'][0])

we = [sum(weights[i] for i in j) for j in w]
        
for j in range(num_bins):
    if b[j] == 1:
        print("Bin {} has items {} for a total weight of {}.".format(j, w[j], we[j]))
print("Total {} bin used.".format(sum(b)))
