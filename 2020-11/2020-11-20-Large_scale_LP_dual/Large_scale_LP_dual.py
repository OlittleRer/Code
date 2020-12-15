
'''
@author: Hsinglu Liu
@version: 1.0
@Date: 2020.8.5
'''

from gurobipy import *
import pandas as pd 
import numpy as np
from pandas import Series, DataFrame
import math

Arcs = {'1,2': [15, 15]    # cost flow 
        ,'1,4': [25, 25]
        ,'1,3': [45, 45]
        ,'2,5': [30, 60]
        ,'2,4': [2, 2]
        ,'5,7': [2, 2]
        ,'4,7': [50, 100]
        ,'4,3': [2, 2]
        ,'3,6': [25, 50]
        ,'6,7': [1, 1]
       }
Arcs

Nodes = [1, 2, 3, 4, 5, 6, 7] 

commodity = [[1, 7, 25],  # s_i, d_i, demand 
             [2, 6, 2]
]


model = Model('MultiCommodity')  

# add variables 
X = {}
for key in Arcs.keys():
    for k in range(len(commodity)):
        key_x = key + ',' + str(k)
        X[key_x] = model.addVar(lb=0
                                ,ub=Arcs[key][1]
                                ,vtype=GRB.CONTINUOUS
                                ,name= 'x_' + key_x 
                               ) 
# add objective function 
obj = LinExpr(0)
for key in Arcs.keys():
    for k in range(len(commodity)):
        key_x = key + ',' + str(k)
        obj.addTerms(Arcs[key][0], X[key_x])
model.setObjective(obj, GRB.MINIMIZE)

# constraints 1 
for k in range(len(commodity)):
    for i in Nodes:
        lhs = LinExpr(0)
        for key_x in X.keys():
#             nodes = key_x.split(',')
            if(i == (int)(key_x.split(',')[0]) and k == (int)(key_x.split(',')[2])):
                lhs.addTerms(1, X[key_x])
            if(i == (int)(key_x.split(',')[1]) and k == (int)(key_x.split(',')[2])):
                lhs.addTerms(-1, X[key_x])
        if(i == commodity[k][0]):
            model.addConstr(lhs == commodity[k][2], name='org_, ' + str(i) + '_' + str(k))
        elif(i == commodity[k][1]): 
            model.addConstr(lhs == -commodity[k][2], name='des_, ' + str(i) + '_' + str(k))
        else:
            model.addConstr(lhs == 0, name='inter_, ' + str(i) + '_' + str(k))
            

# constraints 2  
for key in Arcs.keys():
    lhs = LinExpr(0)
    for k in range(len(commodity)):
        key_x = key + ',' + str(k)
        lhs.addTerms(1, X[key_x])
    model.addConstr(lhs <= Arcs[key][1], name = 'capacity_, ' + key) 

model.write('Multicommodity_model.lp')
model.optimize()

for var in model.getVars():
    if(var.x > 0):
        print(var.varName, '\t', var.x) 
dual = model.getAttr("Pi", model.getConstrs())