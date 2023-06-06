# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:59:49 2023

@author: Joshualiu
"""
import pyomo.environ as pyo
from typing import Dict, Any
import time
from utils import read_3d
from visualtool import palletplot

# Initialise data_dict
def data_reader(instance:str) -> dict:
    
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(instance) 
    
    data_dict: Dict[str, Dict[Any, Any]] = {}

    # Sets
    data_dict["I"] = {
        None: [i for i in range(num_items)]
    }
    data_dict["J"] = {
        None: [j for j in range(num_bins)]
    }

    # Set general parameters
    data_dict["epsilon"] = {None: 0.01}
    data_dict["Upsilon"] = {None: 100}
    
    # Items
    data_dict["v"] = {
        i : weights[i] for i in range(num_items)
    }
    data_dict["l"] = {
        i : item_d[i][0] for i in range(num_items)
    }
    data_dict["w"] = {
        i : item_d[i][1] for i in range(num_items)
    }
    data_dict["h"] = {
        i : item_d[i][2] for i in range(num_items)
    }
    
    # Bins
    data_dict["V"] = {
        j : capacities[j] for j in range(num_bins)
    }
    data_dict["L"] = {
        j : bin_d[j][0] for j in range(num_bins)
    }
    data_dict["W"] = {
        j : bin_d[j][1] for j in range(num_bins)
    }
    data_dict["H"] = {
        j : bin_d[j][2] for j in range(num_bins)
    }
    
    return data_dict

'''setup formulation'''
def define_model() -> pyo.AbstractModel:
    
    model = pyo.AbstractModel()

    '''variables'''
    # Set of item
    model.I = pyo.Set()
    # Set of bin
    model.J = pyo.Set()

    # weight of item
    model.v = pyo.Param(model.I)
    # capacity of bin
    model.V = pyo.Param(model.J)
    
    # epsilon - a small value
    model.epsilon = pyo.Param()
    # Upsilon - a large value
    model.Upsilon = pyo.Param()

    # size of item
    model.l = pyo.Param(model.I)
    model.w = pyo.Param(model.I)
    model.h = pyo.Param(model.I)
    # size of bin
    model.L = pyo.Param(model.J)
    model.W = pyo.Param(model.J)
    model.H = pyo.Param(model.J)

    # if item i is in bin j
    model.p = pyo.Var(model.I*model.J, within=pyo.Boolean)
    # if bin j is used
    model.u = pyo.Var(model.J, within=pyo.Boolean)
    
    # location of item
    model.x = pyo.Var(model.I, within=pyo.NonNegativeIntegers)
    model.y = pyo.Var(model.I, within=pyo.NonNegativeIntegers)
    model.z = pyo.Var(model.I, within=pyo.NonNegativeIntegers)
    
    # if item i is on the right of item i'
    model.xp = pyo.Var(model.I*model.I, within=pyo.Boolean)
    # if item i is behind item i'
    model.yp = pyo.Var(model.I*model.I, within=pyo.Boolean)
    # if item i is above item i'
    model.zp = pyo.Var(model.I*model.I, within=pyo.Boolean)

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
        return sum(model.v[i]*model.p[i,j] for i in model.I) <= model.V[j]*model.u[j]
    model.capacity = pyo.Constraint(model.J, rule=cap)
    
    # constraint:items do not exceed their bin size:
    def size_x(model, i):
        return model.x[i] + model.l[i] <= sum(model.L[j]*model.p[i,j] for j in model.J)
    model.size_x = pyo.Constraint(model.I, rule=size_x)
    def size_y(model, i):
        return model.y[i] + model.w[i] <= sum(model.W[j]*model.p[i,j] for j in model.J)
    model.size_y = pyo.Constraint(model.I, rule=size_y)
    def size_z(model, i):
        return model.z[i] + model.h[i] <= sum(model.H[j]*model.p[i,j] for j in model.J)
    model.size_z = pyo.Constraint(model.I, rule=size_z)

    #constraint:there is no overlap:
    def pos(model, i, ip, j):
        if i == ip:
            return pyo.Constraint.Skip
        return (model.xp[i,ip]+model.xp[ip,i]+model.yp[i,ip]+model.yp[ip,i]+model.zp[i,ip]+model.zp[ip,i] >=
               model.p[i,j]+model.p[ip,j]-1)
    model.pos = pyo.Constraint(model.I, model.I, model.J, rule=pos)
    def pos_x(model, i, ip):
        return model.x[ip] + model.l[ip] <= model.x[i] + (1-model.xp[i,ip])*model.Upsilon
    model.pos_x = pyo.Constraint(model.I, model.I, rule=pos_x)
    def pos_xp(model, i, ip):
        return model.x[i] + model.epsilon <= model.x[ip] + model.l[ip] + model.xp[i,ip]*model.Upsilon
    model.pos_xp = pyo.Constraint(model.I, model.I, rule=pos_xp)
    def pos_y(model, i, ip):
        return model.y[ip] + model.w[ip] <= model.y[i] + (1-model.yp[i,ip])*model.Upsilon
    model.pos_y = pyo.Constraint(model.I, model.I, rule=pos_y)
    def pos_yp(model, i, ip):
        return model.y[i] + model.epsilon <= model.y[ip] + model.w[ip] + model.yp[i,ip]*model.Upsilon
    model.pos_yp = pyo.Constraint(model.I, model.I, rule=pos_yp)
    def pos_z(model, i, ip):
        return model.z[ip] + model.h[ip] <= model.z[i] + (1-model.zp[i,ip])*model.Upsilon
    model.pos_z = pyo.Constraint(model.I, model.I, rule=pos_z)

    return model

def write_vars(instance: pyo.AbstractModel):
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

if __name__ == "__main__":
    '''run the formulation'''
    abstract_model = define_model()
    data_path = "input/instance_3d_3.csv"
    num_items, weights, item_d, num_bins, capacities, bin_d = read_3d(data_path)
    instance = abstract_model.create_instance({None: data_reader(data_path)})

    opt = pyo.SolverFactory("glpk")

    opt.options["tmlim"] = 1000
    opt.options["mipgap"] = 0.00001

    start_time = time.time()

    opt.solve(instance, tee=True)

    print("--- %s seconds ---" % (time.time() - start_time))

    var_outputs = write_vars(instance)
    cost = cal_solution_cost(instance)

    bin_usage = [v['value'] for v in var_outputs if v['variable'] == 'u']
    sol_package = [[] for j in bin_usage]
    sol_pacposition = [[] for j in bin_usage]

    for v in var_outputs:
        if v['variable'] == 'p' and v['value'] == 1:
            sol_package[v['index'][1]].append(v['index'][0])
            position_list = [i for i in var_outputs if i['index'] == v['index'][0]]
            sol_pacposition[v['index'][1]].append((position_list[-3]['value'],
                                                   position_list[-2]['value'],
                                                   position_list[-1]['value']))
    
            
    for j in range(num_bins):
        if sol_package[j]:
            we = sum(weights[i] for i in sol_package[j])
            print("Bin {} has items {} for a total weight of {}.".format(j, sol_package[j], we))
            
            size_list = []
            bin_size = (bin_d[j][0],bin_d[j][1],bin_d[j][2])
            for i in sol_package[j]:
                size_list.append((item_d[i][0],item_d[i][1],item_d[i][2]))
            palletplot(bin_size,sol_pacposition[j],sol_package[j],size_list)

    print("Total {} bin used.".format(sum([1 for j in sol_package if j!=[]])))
