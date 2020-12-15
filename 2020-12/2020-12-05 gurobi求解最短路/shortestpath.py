# _*_coding:utf-8 _*_
from __future__ import print_function
from __future__ import division, print_function
from gurobipy import *
import numpy as np
import copy
import time

starttime = time.time()


#返回最优的路线
def reportMIP(model, Routes):
    if model.status == GRB.OPTIMAL:
        print("Best MIP Solution: ", model.objVal, "\n")
        var = model.getVars()
        for i in range(model.numVars):
            if (var[i].x > 0):
                print(var[i].varName, " = ", var[i].x)
                print("Optimal route:", Routes[i])


def getValue(var_dict, nodeNum):
    x_value = np.zeros([nodeNum, nodeNum])
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
    while (count != len(x_value)-1):
        # print('previousPoint: ', previousPoint )
        if (x[previousPoint][count] > 0):
            previousPoint = count
            route_temp.append(previousPoint)
            count = 0
            continue
        else:
            count += 1
    route_temp.append(len(x_value)-1)
    return route_temp

if __name__ == "__main__":


    nodeNum =11

#距离矩阵
    cost =[[0,2,8,1,1000,1000,1000,1000,1000,1000,1000],[2,0,6,1000,1,1000,1000,1000,1000,1000,1000]
           ,[8,6,0,7,5,1,2,1000,1000,1000,1000],[1,1000,7,0,1000,1000,9,100,100,100,100],[100,1,5,100,0,3,100,2,100,100,100]
        ,[100,100,1,100,3,0,4,100,6,100,100],[100,100,2,9,100,4,0,100,3,1,100],[100,100,100,100,2,100,100,0,7,100,9]
        ,[100,100,100,100,100,6,3,7,0,1,2],[100,100,100,100,100,100,1,100,1,0,4],[100,100,100,100,100,100,100,100,9,2,4,0]]
    print("cost", cost)
    model = Model('TSP')

    # creat decision variables，决策变量
    X = {}
    for i in range(nodeNum):
        for j in range(nodeNum):
            if (i != j):
                X[i, j] = model.addVar(vtype=GRB.BINARY
                                       , name='x_' + str(i) + '_' + str(j)
                                       )

    # set objective function，目标函数

    obj = LinExpr(0)
    for key in X.keys():
        i = key[0]
        j = key[1]
        obj.addTerms(cost[key[0]][key[1]], X[key])

    model.setObjective(obj, GRB.MINIMIZE)

    # add constraints 出发点的流量约束

    lhs_1 =LinExpr(0)
    lhs_2 =LinExpr(0)
    for j in range(1, nodeNum-1):
        for i in range(0,nodeNum):
              if i == 0:
                lhs_1.addTerms(1, X[i, j])
    model.addConstr(lhs_1 == 1, name='visit_' + str(i)+"start")

    #终点的流量约束
    for i in range(1,nodeNum-1):
        for j in range(1, nodeNum):
              if j == nodeNum-1:
                  lhs_2.addTerms(1, X[i, j])
    model.addConstr(lhs_2 == 1, name='visit_' + str(j) + "end")

    #其余点的流量约束
    for j in range(1,nodeNum-1):
        lhs3 = LinExpr(0)
        for i in range(0, nodeNum-1):
            if i != j:
                lhs3.addTerms(1, X[i, j])
        for i in range(1, nodeNum):
            if i != j:
                lhs3.addTerms(-1, X[j, i])
        model.addConstr(lhs3 == 0, name='visit_' + str(j)+'balance_flow')

    model.write('modelshortestpath.lp')
    model.setParam(GRB.Param.MIPGap, 0)
    model.setParam(GRB.Param.TimeLimit, 60)
    model.optimize()
    # 可以输出求解的决策变量
    print(model.ObjVal)
    X_NEW={}
    for var in model.getVars():
        if (var.x > 0):
            print(var.varName, '\t', var.x)
            X_NEW[var.varName]=var.x

    x_value = getValue(X, nodeNum)
    route = getRoute(x_value)
    print('optimal route:', route)


