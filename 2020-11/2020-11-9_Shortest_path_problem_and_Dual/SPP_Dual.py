'''
@author: Hsinglu Liu
@version: 1.0
@Date: 2019.5.5
'''

from gurobipy import *
import pandas as pd 
import numpy as np 

Nodes = ['s', 'a', 'b', 'c', 't'] 

Arcs = {('s','a'): 5 
        ,('s','b'): 8
        ,('a','c'): 2
        ,('b','a'): -10
        ,('c','b'): 3
        ,('b','t'): 4
        ,('c','t'): 3
       }
Arcs

model = Model('dual problem') 

pi_a = model.addVar(lb=-1000, ub=1000, vtype=GRB.CONTINUOUS, name= "pi_a") 
pi_b = model.addVar(lb=-1000, ub=1000, vtype=GRB.CONTINUOUS, name= "pi_b") 
pi_c = model.addVar(lb=-1000, ub=1000, vtype=GRB.CONTINUOUS, name= "pi_c") 
pi_s = model.addVar(lb=-1000, ub=1000, vtype=GRB.CONTINUOUS, name= "pi_s")  
pi_t = model.addVar(lb=-1000, ub=1000, vtype=GRB.CONTINUOUS, name= "pi_t") 

obj = LinExpr(0) 
obj.addTerms(1 , pi_s)
obj.addTerms(1 , pi_t)
model.setObjective(obj, GRB.MAXIMIZE) 

# lhs relation , rhs 
model.addConstr(pi_s - pi_a <= 5)
model.addConstr(pi_s - pi_b <= 8)
model.addConstr(pi_t + pi_c <= 3)
model.addConstr(pi_t + pi_b <= 4) 
model.addConstr(pi_b - pi_a <= -10)
model.addConstr(pi_a - pi_c <= 2)
model.addConstr(pi_c - pi_b <= 3)

model.write('model2.lp')
model.optimize()

print(model.ObjVal) 
for var in model.getVars():
    print(var.varName, '\t', var.x) 










