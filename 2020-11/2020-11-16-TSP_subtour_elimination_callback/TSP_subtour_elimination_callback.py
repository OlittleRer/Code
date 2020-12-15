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
    # 假如是5个点的算例，我们的路径会是1-4-2-3-5-6这样的，因为我们加入了一个虚拟点
    # 也就是当路径长度为6的时候，我们就停止，这个长度和x_value的长度相同
    x = copy.deepcopy(x_value)
#     route_temp.append(0)
    previousPoint = 0
    arcs = []
    route_temp = [previousPoint] 
    count = 0 
    while(len(route_temp) < len(x) and count < len(x)): 
        print('previousPoint: ', previousPoint, 'count: ', count)
        if(x[previousPoint][count] > 0): 
            previousPoint = count  
            route_temp.append(previousPoint) 
            count = 0 
            continue
        else:
            count += 1
    return route_temp         

# cost = [[0, 7, 2, 1, 5], 
#         [7, 0, 3, 6, 8],
#         [2, 3, 0, 4, 2],
#         [1, 6, 4, 0, 9],
#         [5, 8, 2, 9, 0]]

# Callback - use lazy constraints to eliminate sub-tours

# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where): 
    if(where == GRB.Callback.MIPSOL): 
        # make a list of edges selected in the solution
        print('model._vars', model._vars)
#         vals = model.cbGetSolution(model._vars)
        x_value = np.zeros([nodeNum + 1, nodeNum + 1]) 
        for m in model.getVars():
            if(m.varName.startswith('x')):
#                 print(var[i].varName)
#                 print(var[i].varName.split('_'))
                a = (int)(m.varName.split('_')[1])  
                b = (int)(m.varName.split('_')[2])
                x_value[a][b] = model.cbGetSolution(m) 
        print("solution = ", x_value)
#         print('key = ', model._vars.keys())
#         selected = []
#         for i in range(nodeNum):
#             for j in range(nodeNum):
#                 if(i != j and x_value[i][j] > 0.5):
#                     selected.append((i, j))
#         selected = tuplelist(selected)
# #         selected = tuplelist((i,j) for i in range(nodeNum), for if x_value[i][j] > 0.5)
#         print('selected = ', selected)
        # find the shortest cycle in the selected edge list
        tour = subtour(x_value)
        print('tour = ', tour) 
        if(len(tour) < nodeNum + 1):  
            # add subtour elimination constraint for every pair of cities in tour
            print("---add sub tour elimination constraint--")
#             model.cbLazy(quicksum(model._vars[i][j]
#                                       for i in tour
#                                       for j in tour
#                                       if i != j)
#                              <= len(tour)-1)
#             LinExpr = quicksum(model._vars[i][j]
#                                       for i in tour
#                                       for j in tour
#                                       if i != j)
            for i,j in itertools.combinations(tour, 2):
                print(i,j) 
    
            model.cbLazy(quicksum(model._vars[i, j]
                                      for i,j in itertools.combinations(tour, 2))
                             <= len(tour)-1)
            LinExpr = quicksum(model._vars[i, j]
                                      for i,j in itertools.combinations(tour, 2))
            print('LinExpr = ', LinExpr)
            print('RHS = ', len(tour)-1)  

# compute the degree of each node in given graph 
def computeDegree(graph):
    degree = np.zeros(len(graph))
    for i in range(len(graph)):
        for j in range(len(graph)):
            if(graph[i][j] > 0.5):
                degree[i] = degree[i] + 1
                degree[j] = degree[j] + 1
    print('degree', degree)
    return degree 

# given a graph, get the edges of this graph  
def findEdges(graph):
    edges = []
    for i in range(1, len(graph)):
        for j in range(1, len(graph)):
            if(graph[i][j] > 0.5):
                edges.append((i, j))
    
    return edges 



# Given a tuplelist of edges, find the shortest subtour
def subtour(graph):
    # compute degree of each node
    degree = computeDegree(graph)
    unvisited = []
    for i in range(1, len(degree)):
        if(degree[i] >= 2):
            unvisited.append(i)
    cycle = range(0, nodeNum + 1) # initial length has 1 more city
    
    edges = findEdges(graph)
    edges = tuplelist(edges)
    print(edges)
    while unvisited: # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:  # true if neighbors is non-empty
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
            neighbors2 = [i for i,j in edges.select('*',current) if i in unvisited]
            if(neighbors2):
                neighbors.extend(neighbors2)
#             print('current:', current, '\n neighbors', neighbors)
        
        isLink = ((thiscycle[0], thiscycle[-1]) in edges) or ((thiscycle[-1], thiscycle[0]) in edges)
        if(len(cycle) > len(thiscycle) and len(thiscycle) >= 3 and isLink):
#             print('in = ', ((thiscycle[0], thiscycle[-1]) in edges) or ((thiscycle[-1], thiscycle[0]) in edges))
            cycle = thiscycle
            return cycle
    return cycle
	
	
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

# model.addConstr(X[0, nodeNum] == 0, name = 'visit_' + str(0) + ',' + str(nodeNum)) 

# set lazy constraints 
model._vars = X 
model.Params.lazyConstraints = 1
model.optimize(subtourelim)
# subProblem.optimize() 
x_value = getValue(X, nodeNum) 
# route = getRoute(x_value)
# print('optimal route:', route)


	
	
	

