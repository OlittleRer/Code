# _*_coding:utf-8 _*_
'''
@author: Hsinglu Liu
@version: 1.0
@Date: 2019.5.5
'''

# _*_coding:utf-8 _*_
'''
@author: Hsinglu Liu
@version: 1.0
@Date: 2019.5.5
'''

from __future__ import print_function
from __future__ import division, print_function
from gurobipy import *
import re;
import math;
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from matplotlib.lines import lineStyles
import time

starttime = time.time()

# function to read data from .txt files   
def readData(path, nodeNum):
    nodeNum = nodeNum;
    cor_X = []
    cor_Y = []
    
    f = open(path, 'r');
    lines = f.readlines();
    count = 0;
    # read the info
    for line in lines:
        count = count + 1;
        if(count >= 10 and count <= 10 + nodeNum):
            line = line[:-1]
            str = re.split(r" +", line)
            cor_X.append(float(str[2]))
            cor_Y.append(float(str[3]))
                
    # compute the distance matrix
    disMatrix = [([0] * nodeNum) for p in range(nodeNum)]; # 初始化距离矩阵的维度,防止浅拷贝
    # data.disMatrix = [[0] * nodeNum] * nodeNum]; 这个是浅拷贝，容易重复
    for i in range(0, nodeNum):
        for j in range(0, nodeNum):
            temp = (cor_X[i] - cor_X[j])**2 + (cor_Y[i] - cor_Y[j])**2;
            disMatrix[i][j] = (int)(math.sqrt(temp));
#             disMatrix[i][j] = 0.1 * (int)(10 * math.sqrt(temp));
#             if(i == j):
#                 data.disMatrix[i][j] = 0;
#             print("%6.0f" % (math.sqrt(temp)), end = " ");
            temp = 0;
    
    return disMatrix;

def printData(disMatrix):
    print("-------cost matrix-------\n");
    for i in range(len(disMatrix)):
        for j in range(len(disMatrix)):
            #print("%d   %d" % (i, j));
            print("%6.1f" % (disMatrix[i][j]), end = " ");
#             print(disMatrix[i][j], end = " ");
        print();
        
def reportMIP(model, Routes):
    if model.status == GRB.OPTIMAL:
        print("Best MIP Solution: ", model.objVal, "\n")
        var = model.getVars()
        for i in range(model.numVars):
            if(var[i].x > 0):
                print(var[i].varName, " = ", var[i].x)
                print("Optimal route:", Routes[i])
                     
def getValue(var_dict, nodeNum): 
    x_value = np.zeros([nodeNum + 1, nodeNum + 1]) 
    for key in var_dict.keys():   
        a = key[0]
        b = key[1]
        x_value[a][b] = var_dict[key].x  
            
    return x_value    

def getRoute(x_value):
	'''
	input: x_value的矩阵
	output:一条路径，[0, 4, 3, 7, 1, 2, 5, 8, 9, 6, 0]，像这样
	'''
    # 假如是5个点的算例，我们的路径会是1-4-2-3-5-6这样的，因为我们加入了一个虚拟点
    # 也就是当路径长度为6的时候，我们就停止，这个长度和x_value的长度相同
    x = copy.deepcopy(x_value)
#     route_temp.append(0)
    previousPoint = 0
    route_temp = [previousPoint] 
    count = 0 
    while(len(route_temp) < len(x)): 
        #print('previousPoint: ', previousPoint )
        if(x[previousPoint][count] > 0): 
            previousPoint = count  
            route_temp.append(previousPoint) 
            count = 0 
            continue
        else:
            count += 1
    return route_temp
'''
# toy example
cost = [[0, 7, 2, 1, 5], 
        [7, 0, 3, 6, 8],
        [2, 3, 0, 4, 2],
        [1, 6, 4, 0, 9],
        [5, 8, 2, 9, 0]]   
''' 


# nodeNum = 5 
nodeNum = 10 
path = 'solomon-100/in/c201.txt';
cost = readData(path, nodeNum)
printData(cost)


model = Model('TSP')

# creat decision variables 
X = {} 
mu = {}  
for i in range(nodeNum + 1):  
    mu[i] = model.addVar(lb = 0.0
                         , ub = 100 #GRB.INFINITY
                          # , obj = distance_initial
                         , vtype = GRB.CONTINUOUS
                         , name = "mu_" + str(i)  
                        )

    for j in range(nodeNum + 1): 
        if(i != j):
            X[i, j] = model.addVar(vtype = GRB.BINARY
                                  , name = 'x_' + str(i) + '_' + str(j) 
                                  )

# set objective function
obj = LinExpr(0)
for key in X.keys():
    i = key[0]
    j = key[1]
    if(i < nodeNum and j < nodeNum):
        obj.addTerms(cost[key[0]][key[1]], X[key])
    elif(i == nodeNum):
        obj.addTerms(cost[0][key[1]], X[key])
    elif(j == nodeNum):
        obj.addTerms(cost[key[0]][0], X[key])
        
model.setObjective(obj, GRB.MINIMIZE)

# add constraints 1 
for j in range(1, nodeNum + 1): 
    lhs = LinExpr(0)
    for i in range(0, nodeNum): 
        if(i != j):
            lhs.addTerms(1, X[i, j])
    model.addConstr(lhs == 1, name = 'visit_' + str(j))

# add constraints 2
for i in range(0, nodeNum):
    lhs = LinExpr(0)
    for j in range(1, nodeNum + 1): 
        if(i != j):
            lhs.addTerms(1, X[i, j])
    model.addConstr(lhs == 1, name = 'visit_' + str(j))

# add MTZ constraints
# for key in X.keys():
#     org = key[0]
#     des = key[1]
#     if(org != 0 or des != 0):
# #         pass 
#         model.addConstr(mu[org] - mu[des] + 100 * X[key] <= 100 - 1) 
for i in range(0, nodeNum):
    for j in range(1, nodeNum + 1):
        if(i != j):
            model.addConstr(mu[i] - mu[j] + 100 * X[i, j] <= 100 - 1) 

model.write('model.lp')  
model.optimize()

x_value = getValue(X, nodeNum) 
route = getRoute(x_value)
print('optimal route:', route) 