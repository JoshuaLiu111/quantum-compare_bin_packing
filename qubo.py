# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:37:27 2023

@author: Joshualiu
"""

from docplex.mp.model import Model

from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.translators import from_docplex_mp

from qiskit.utils import algorithm_globals
from qiskit.primitives import Sampler
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.algorithms.optimizers import SPSA
from utils import read_instance

num_items, num_bins, weights, capacities = read_instance() 

I = range(num_items)
J = range(num_bins)
# Formulate the problem as a Docplex model
model = Model()

# if box i is in bin j
x = model.binary_var_dict((i, j) for i in I for j in J)
# if bin j is used
u = model.binary_var_dict(j for j in J)

# objective:minimize the number of bin used
model.minimize(model.sum(u[j] for j in J))

# constraint:each item is allocated to exactly one bin:
for i in I:
    model.add(model.sum(x[i,j] for j in J) == 1)
    
# constraint:maximum capacity of each bin j cannot be exceeded:
for j in J:
    model.add(model.sum(weights[i]*x[i,j] for i in I) <= capacities[j]*u[j])

# Convert the Docplex model into a `QuadraticProgram` object
problem = from_docplex_mp(model)

# Run quantum algorithm QAOA on qasm simulator
seed = 111
algorithm_globals.random_seed = seed

spsa = SPSA(maxiter=10)
sampler = Sampler()
qaoa = QAOA(sampler=sampler, optimizer=spsa, reps=2)
algorithm = MinimumEigenOptimizer(qaoa)
result = algorithm.solve(problem)
print(result.prettyprint()) 