# _*_coding:utf-8 _*_
from __future__ import print_function
from gurobipy import *
import re 
import math 
# from test.pickletester import BigmemPickleTests 
import matplotlib.pyplot as plt
import numpy
import pandas as pd

class Data:
    customerNum = 0 
    nodeNum     = 0 
    range       = 0 
    lunchingTime= 0 
    recoverTime = 0 
    cor_X       = [] 
    cor_Y       = [] 
    demand      = [] 
    serviceTime = [] 
    readyTime   = [] 
    dueTime     = [] 
    disMatrix   = [[]] # 读取数据
    
# function to read data from .txt files   
def readData(data, path, customerNum):
    data.customerNum = customerNum 
    data.nodeNum = customerNum + 2 
    f = open(path, 'r') 
    lines = f.readlines() 
    count = 0 
    # read the info
    for line in lines:
        count = count + 1 
        if(count == 2):
            line = line[:-1] 
            str = re.split(r" +", line) 
            data.range = float(str[0]) 
        elif(count == 5):
            line = line[:-1] 
            str = re.split(r" +", line) 
            data.lunchingTime = float(str[0]) 
            data.recoverTime = float(str[1]) 
        elif(count >= 9 and count <= 9 + customerNum): # (count >= 9 and count <= 9 + customerNum)
            line = line[:-1] 
            str = re.split(r" +", line) 
            data.cor_X.append(float(str[2])) 
            data.cor_Y.append(float(str[3])) 
            data.demand.append(float(str[4])) 
            data.readyTime.append(float(str[5])) 
            data.dueTime.append(float(str[6])) 
            data.serviceTime.append(float(str[7])) 

    data.cor_X.append(data.cor_X[0]) 
    data.cor_Y.append(data.cor_Y[0]) 
    data.demand.append(data.demand[0]) 
    data.readyTime.append(data.readyTime[0]) 
    data.dueTime.append(data.dueTime[0]) 
    data.serviceTime.append(data.serviceTime[0]) 
    
            
    # compute the distance matrix
    data.disMatrix = [([0] * data.nodeNum) for p in range(data.nodeNum)]  # 初始化距离矩阵的维度,防止浅拷贝
    # data.disMatrix = [[0] * nodeNum] * nodeNum]  这个是浅拷贝，容易重复
    for i in range(0, data.nodeNum):
        for j in range(0, data.nodeNum):
            temp = (data.cor_X[i] - data.cor_X[j])**2 + (data.cor_Y[i] - data.cor_Y[j])**2 
            data.disMatrix[i][j] = math.sqrt(temp) 
#             if(i == j):
#                 data.disMatrix[i][j] = 0 
            # print("%6.2f" % (math.sqrt(temp)), end = " ") 
            temp = 0 
    
    return data 
            
        
def printData(data, customerNum):
    print("下面打印数据\n") 
    print("UAV range = %4d" % data.range) 
    print("UAV lunching time = %4d" % data.lunchingTime) 
    print("UAV recover time = %4d" % data.recoverTime) 
    for i in range(len(data.demand)):
        print('{0}\t{1}\t{2}\t{3}'.format(data.demand[i], data.readyTime[i],data.dueTime[i],  data.serviceTime[i])) 
    
    print("-------距离矩阵-------\n") 
    for i in range(data.nodeNum):
        for j in range(data.nodeNum):
            #print("%d   %d" % (i, j)) 
            print("%6.2f" % (data.disMatrix[i][j]), end = " ") 
        print() 

class Solution:
    ObjVal = 0 
    X = [[]] 
    Y = [[[]]] 
    U = [] 
    P = [] 
    T = [] 
    Tt = [] 
    route_Truck = [] 
    route_UAV = [] 
    
#     def __init__(self):
#         solution = Solution() 
#         # X_ij
#         solution.X = [[[] for i in range(data.nodeNum)] for j in range(data.nodeNum)]  
#         # Y_ijk
#         solution.Y = [[[[] for k in range(data.nodeNum)] for j in range(data.nodeNum)] for i in range(data.nodeNum)] 
#         # U_i
#         solution.U = [[] for i in range(data.nodeNum)] 
#         # P_ij
#         solution.P = [[[] for j in range(data.nodeNum)] for i in range(data.nodeNum)] 
#         # T_i, T_i'
#         solution.T = [[] for i in range(data.nodeNum)] 
#         solution.Tt = [[] for i in range(data.nodeNum)] 
#         return solution 
    
    def getSolution(self, data, model):
        solution = Solution() 
        solution.ObjVal = model.ObjVal 
        # X_ij
        solution.X = [([0] * data.nodeNum) for j in range(data.nodeNum)]  
        # Y_ijk
        solution.Y = [[([0] * data.nodeNum) for j in range(data.nodeNum)] for i in range(data.nodeNum)] 
        # U_i
        solution.U = [[0] for i in range(data.nodeNum)] 
        # P_ij
        solution.P = [[[0] for j in range(data.nodeNum)] for i in range(data.nodeNum)] 
        # T_i, T_i'
        solution.T = [[0] for i in range(data.nodeNum)] 
        solution.Tt = [[0] for i in range(data.nodeNum)] 
        
        a = U[0].x 
        for m in model.getVars():
            str = re.split(r"_", m.VarName) 
            if(str[0] == "X" and m.x == 1):
                solution.X[int(str[1])][int(str[2])] = m.x 
                print(str, end = "") 
                print(" = %d" % m.x) 
            elif(str[0] == "Y" and m.x == 1):
                solution.Y[int(str[1])][int(str[2])][int(str[3])] = m.x 
            elif(str[0] == "U" and m.x > 0) :
                solution.U[int(str[1])] = m.x 
            elif(str[0] == "T" and m.x > 0):
                solution.T[int(str[1])] = m.x  
            elif(str[0] == "Tt" and m.x > 0):
                solution.Tt[int(str[1])] = m.x 
            elif(str[0] == "P" and m.x > 0):
                solution.P[int(str[1])][int(str[2])] = m.x   
        
        # get the route of truck and UAV
        j = 0 
        for i in range(data.nodeNum):
            i = j   # note that the variable is whether is a local variable or a global variable
            # print("i = %d, j = %d" % (i, j), end = "        ") 
            for j in range(data.nodeNum):
                if(solution.X[i][j] == 1):
                    solution.route_Truck.append(i) 
                    print(" %d -" % i, end = " ") 
                    # print("   i = %d, j = %d" % (i, j)) 
                    break 
        print(" 0")  
        solution.route_Truck.append(0) 

        print("\n\n ------Route of UAV ------- ") 
        count = 0 
        for i in range(data.nodeNum):
            for j in range(data.nodeNum):
                for k in range(data.nodeNum):
                    if(solution.Y[i][j][k] == 1):
                        count  = count + 1 
                        #print("UAV %d : %d - %d - %d" % (count, i, j, k))    
                        temp = [i, j, k] 
                        solution.route_UAV.append(temp) 
        
        for i in range(len(solution.route_Truck)):
            print(" %d " %  solution.route_Truck[i], end = " ") 
        print() 
        
        print("\n\n ------Route of UAV ------- ") 
        for i in range(len(solution.route_UAV)):
            for j in range(len(solution.route_UAV[0])):
                print("UAV %d : %d - %d - %d" % (i, solution.route_UAV[i][0], solution.route_UAV[i][1], solution.route_UAV[i][2]))    

        # print(solution.route_UAV)     
        
        return solution  
                
                                                         
# reading data
data = Data() 
# path = r'C:\Users\hsingluLiu\eclipse-workspace\PythonCallGurobi_Applications\FSTSP\c101.txt' 
path = 'c101.txt' 

customerNum = 10  
readData(data, path, customerNum) 
printData(data, customerNum) 


# =========build the model===========
big_M = 10000 
# construct the model object
model = Model("FSTSP") 

# Initialize variables
# create variables: Muiti-dimension vector: from inner to outer
# X_ij
X = [[[] for i in range(data.nodeNum)] for j in range(data.nodeNum)]  

# Y_ijk
Y = [[[[] for k in range(data.nodeNum)] for j in range(data.nodeNum)] for i in range(data.nodeNum)] 

# U_i
U = [[] for i in range(data.nodeNum)] 

# P_ij
P = [[[] for j in range(data.nodeNum)] for i in range(data.nodeNum)] 

# T_i, T_i'
T = [[] for i in range(data.nodeNum)] 
Tt = [[] for i in range(data.nodeNum)] 

for i in range(data.nodeNum):
    name1 = 'U_' + str(i) 
    name2 = 'T_' + str(i) 
    name3 = 'Tt_' + str(i) 
    U[i] = model.addVar(0, data.nodeNum, vtype = GRB.CONTINUOUS, name = name1) 
    T[i] = model.addVar(0, big_M, vtype = GRB.CONTINUOUS, name = name2) 
    Tt[i] = model.addVar(0, big_M, vtype = GRB.CONTINUOUS, name = name3) 
    for j in range(data.nodeNum):
        name4 = 'X_' + str(i) + "_"+ str(j) 
        name5 = 'P_' + str(i) + "_" + str(j) 
        X[i][j] = model.addVar(0, 1, vtype = GRB.BINARY, name = name4) 
        P[i][j] = model.addVar(0, 1, vtype = GRB.BINARY, name = name5) 
        for k in range(data.nodeNum):
            name6 = 'Y_' + str(i) + "_" + str(j) + "_" + str(k) 
            Y[i][j][k] = model.addVar(0, 1, vtype = GRB.BINARY, name = name6) 

# Add constraints
# create the objective expression(1)
obj = LinExpr(0) 
            
# add the objective function into the model        
model.setObjective(T[data.nodeNum - 1], GRB.MINIMIZE) 

# constraint (2)
for j in range(1, data.nodeNum - 1): # 这里需要注意，i的取值范围，否则可能会加入空约束 
    expr = LinExpr(0) 
    for i in range(0, data.nodeNum - 1): # i -- N0
        if(i != j):
            expr.addTerms(1, X[i][j]) 
            for k in range(1, data.nodeNum): # k -- N+
                if(i != k and j != k):
                    expr.addTerms(1, Y[i][j][k]) 

    model.addConstr(expr == 1, "c1") 
    expr.clear() 
        

# constraint (3)
expr = LinExpr(0) 
for j in range(1, data.nodeNum):
    expr.addTerms(1, X[0][j]) 
model.addConstr(expr == 1, "c2") 
expr.clear() 

# constraint (4)
expr = LinExpr(0) 
for i in range(data.nodeNum - 1):
    expr.addTerms(1, X[i][data.nodeNum - 1]) 
model.addConstr(expr == 1.0, "c3") 
expr.clear() 

# constraint (5)
for i in range(1, data.nodeNum - 1):
    for j in range(1, data.nodeNum):
        if(i != j):
            model.addConstr(U[i] - U[j] + 1 <= big_M  - big_M * X[i][j], 'c5') 
            
   
# constraint (6)
for j in range(1, data.nodeNum - 1):
    expr1 = LinExpr(0) 
    expr2 = LinExpr(0) 
    for i in range(0, data.nodeNum - 1):
        if(j != i):
            expr1.addTerms(1, X[i][j]) 
               
    for k in range(1, data.nodeNum):
        if(j != k):
            expr2.addTerms(1, X[j][k]) 
               
    model.addConstr(expr1 == expr2, "c6") 
    expr1.clear() 
    expr2.clear() 

# constraint (7)
for i in range(data.nodeNum - 1):
    expr = LinExpr(0) 
    for j in range(1, data.nodeNum - 1):
        if(i != j ):
            for k in range(1, data.nodeNum):
                if(i != k and j != k):
                    expr.addTerms(1, Y[i][j][k]) 
    model.addConstr(expr <= 1, 'c7') 
    expr.clear()         

# constraint (8)
for k in range(1, data.nodeNum):
    expr = LinExpr(0) 
    for i in range(0, data.nodeNum - 1):
        if(i != k ):
            for j in range(1, data.nodeNum - 1):
                if(j != i and j != k):
                    expr.addTerms(1, Y[i][j][k]) 
    model.addConstr(expr <= 1, 'c8') 
    expr.clear() 
    
# constraint (9)
for i in range(1, data.nodeNum - 1):
    for j in range(1, data.nodeNum):
        for k in range(1, data.nodeNum):
            if(i != j and i != k and j != k):
                expr1 = LinExpr(0) 
                expr2 = LinExpr(0) 
                for h in range(data.nodeNum - 1):
                    if(h != i):
                        expr1.addTerms(1, X[h][i]) 
                for l in range(1, data.nodeNum - 1):
                    if(l != k):
                        expr2.addTerms(1, X[l][k]) 
                model.addConstr(2 * Y[i][j][k] <= expr1 + expr2, "c9") 
                expr1.clear() 
                expr2.clear() 

# constraint (10)
for j in range(1, data.nodeNum - 1):
    for k in range(1, data.nodeNum):
        if(j != k):
            expr = LinExpr(0) 
            for h in range(1, data.nodeNum - 1):
                expr.addTerms(1, X[h][k]) 
            model.addConstr(Y[0][j][k] <= expr, "c10") 
            expr.clear() 

# constraint (11)
for i in range(1, data.nodeNum - 1):
    for k in range(1, data.nodeNum):
        if(k != i):
            expr = LinExpr(0) 
            for j in range(1, data.nodeNum - 1):
                if(i != j and j != k):
                    expr.addTerms(big_M, Y[i][j][k]) 
            model.addConstr(U[k] - U[i] >= 1 - big_M + expr, "c11") 
            expr.clear() 

# constraint (12)
for i in range(1, data.nodeNum - 1):
    expr = LinExpr(0) 
    for j in range(1, data.nodeNum - 1):
        for k in range(1, data.nodeNum):
            if(j != i and i != k and j != k):
                expr.addTerms(big_M, Y[i][j][k]) 
    model.addConstr(Tt[i] >= T[i] - big_M + expr, "c12") 
    expr.clear() 

# constraint (13)
for i in range(1, data.nodeNum - 1):
    expr = LinExpr(0) 
    for j in range(1, data.nodeNum - 1):
        for k in range(1, data.nodeNum):
            if(j != i and i != k and j != k):
                expr.addTerms(big_M, Y[i][j][k]) 
    model.addConstr(Tt[i] <= T[i] + big_M - expr, "c13") 
    expr.clear() 

# constraint (14)
for k in range(1, data.nodeNum):
    expr = LinExpr(0) 
    for i in range(0, data.nodeNum - 1):
        for j in range(1, data.nodeNum - 1):
            if(j != i and i != k and j != k):
                expr.addTerms(big_M, Y[i][j][k]) 
    model.addConstr(Tt[k] >= T[k] - big_M + expr, "c14") 
    expr.clear()             

# constraint (15)
for k in range(1, data.nodeNum):
    expr = LinExpr(0) 
    for i in range(0, data.nodeNum - 1):
        for j in range(1, data.nodeNum - 1):
            if(j != i and i != k and j != k):
                expr.addTerms(big_M, Y[i][j][k]) 
    model.addConstr(Tt[k] <= T[k] + big_M - expr, "c15") 
    expr.clear()    

# constraint (16)
for h in range(data.nodeNum - 1):
    for k in range(1, data.nodeNum):
        if(h != k):
            expr1 = LinExpr(0) 
            expr2 = LinExpr(0) 
            for l in range(1, data.nodeNum - 1):
                for m in range(1, data.nodeNum):
                    if(k != l and k != m and l != m):
                        expr1.addTerms(data.lunchingTime, Y[k][l][m]) 
            
            for i in range(data.nodeNum - 1):
                for j in range(1, data.nodeNum - 1):
                    if(i != j and i != k and j != k):
                        expr2.addTerms(data.recoverTime, Y[i][j][k]) 
            model.addConstr(T[k] >= T[h] + data.disMatrix[h][k] + expr1 + expr2 - big_M + big_M * X[h][k], "c16") 
            expr1.clear() 
            expr2.clear() 

# constraint (17)
for j in range(1, data.nodeNum - 1):
    for i in range(data.nodeNum - 1):
        if(i != j):
            expr = LinExpr(0) 
            for k in range(1, data.nodeNum):
                if(i != k and j != k):
                    expr.addTerms(big_M, Y[i][j][k]) 
            model.addConstr(Tt[j] >= Tt[i] + data.disMatrix[i][j] - big_M + expr, "c17") 
            expr.clear() 

# constraint (18)
for j in range(1, data.nodeNum - 1):
    for k in range(1, data.nodeNum):
        if(k != j):
            expr = LinExpr(0) 
            for i in range(data.nodeNum - 1):
                if(i != k and i != j):
                    expr.addTerms(big_M, Y[i][j][k]) 
            model.addConstr(Tt[k] >= Tt[j] + data.disMatrix[j][k] + data.recoverTime - big_M + expr, "c18") 
            expr.clear() 

# constraint (19)
for k in range(1, data.nodeNum):
    for j in range(1, data.nodeNum - 1):
        for i in range(data.nodeNum - 1):
            if(i != j and i != k and j != k):
                model.addConstr(Tt[k] - Tt[j] + data.disMatrix[i][j] <= data.range + big_M - big_M * Y[i][j][k], "c19") 

# constraint (20)
for i in range(1, data.nodeNum - 1):
    for j in range(1, data.nodeNum - 1):
        if(i != j):
            model.addConstr(U[i] - U[j] >= 1 - big_M * P[i][j], "c20") 

# constraint (21)
for i in range(1, data.nodeNum - 1):
    for j in range(1, data.nodeNum - 1):
        if(i != j):
            model.addConstr(U[i] - U[j] <= -1 +big_M - big_M * P[i][j], "c21") 

# constraint (22)
for i in range(1, data.nodeNum - 1):
    for j in range(1, data.nodeNum - 1):
        if(i != j):
            model.addConstr(P[i][j] + P[j][i] == 1, "c22") 

# constraint (23)
for i in range(data.nodeNum - 1):
    for k in range(1, data.nodeNum):
        for l in range(1, data.nodeNum - 1):
            if(k != i and l != i and l != k):
                expr1 = LinExpr(0) 
                expr2 = LinExpr(0) 
                for j in range(1, data.nodeNum - 1):
                    if(k != j and i != j):
                        expr1.addTerms(big_M, Y[i][j][k]) 
                for m in range(1, data.nodeNum - 1):
                    for n in range(1, data.nodeNum):
                        if(l != m and l != n and m != n):
                            expr2.addTerms(big_M, Y[l][m][n]) 
                model.addConstr(Tt[l] >= Tt[k] - 3*big_M + expr1 + expr2 + big_M * P[i][l], "c23") 
                expr1.clear() 
                expr2.clear() 

# constraint (24)
model.addConstr(T[0] == 0, "c24") 

# constraint (25)
model.addConstr(Tt[0] == 0, "c25") 

# constraint (26)
for j in range(1, data.nodeNum - 1):
    model.addConstr(P[0][j] == 1, "c26") 

# constraint (27)
for i in range(data.nodeNum):
    for j in range(data.nodeNum):
        if(i == j):
            model.addConstr(X[i][j] == 0, "c27") 
        for k in range(data.nodeNum):
            if(i == j or i == k or k == j):
                model.addConstr(Y[i][j][k] == 0, "c28") 
                      

# solve the problem
model.write('a.lp')
model.Params.timelimit = 3600 
model.optimize() 


# get the solution info
solution = Solution() 
solution = solution.getSolution(data, model) 
print("\n\n\n\n-----optimal value-----")
print("Obj: %g" % solution.ObjVal) 
print("\n\n ------Route of truck------") 
# print("Truck: ", end = " ") 
j = 0 
for i in range(data.nodeNum):
    i = j   # note that the variable is whether is a local variable or a global variable
    # print("i = %d, j = %d" % (i, j), end = "        ") 
    for j in range(data.nodeNum):
        if(solution.X[i][j] == 1):
            print(" %d -" % i, end = " ") 
            # print("   i = %d, j = %d" % (i, j)) 
            break 
print(" 0")  

print("\n\n ------Route of UAV ------- ") 
count = 0 
for i in range(data.nodeNum):
    for j in range(data.nodeNum):
        for k in range(data.nodeNum):
            if(solution.Y[i][j][k] == 1):
                count  = count + 1 
                print("UAV %d : %d - %d - %d" % (count, i, j, k)) 


# draw the route graph
# draw all the nodes first
# data1 = Data() 
# readData(data1, path, 100) 
fig = plt.figure(figsize=(15,10)) 
font_dict = {'family': 'Arial',   # serif
         'style': 'normal',   # 'italic',
         'weight': 'normal',
        'color':  'darkred', 
        'size': 30,
        }
font_dict2 = {'family': 'Arial',   # serif
         'style': 'normal',   # 'italQic',
         'weight': 'normal',
        'color':  'darkred', 
        'size': 24,
        }
plt.xlabel('x', font_dict) 
plt.ylabel('y', font_dict)
plt.title('Optimal Solution for FSTSP (5 customers)', font_dict)  
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)    # plt.yticks(fontsize=30) 
plt.grid(True, color='r', linestyle='-', linewidth=2)


'''
marker='o'
marker=','
marker='.'
marker=(9, 3, 30)
marker='+'
marker='v'
marker='^'
marker='<'
marker='>'
marker='1'
marker='2'
marker='3'
red        blue        green
'''
plt.scatter(data.cor_X[0], data.cor_Y[0], c='blue', alpha=1, marker=',', linewidths=5, label='depot')
plt.scatter(data.cor_X[1:-1], data.cor_Y[1:-1], c='magenta', alpha=1, marker='o', linewidths=5, label='customer') # c='red'定义为红色，alpha是透明度，marker是画的样式

# draw the route
for i in range(data.nodeNum):
    for j in range(data.nodeNum):
        if(solution.X[i][j] == 1):
            x = [data.cor_X[i], data.cor_X[j]] 
            y = [data.cor_Y[i], data.cor_Y[j]] 
            plt.plot(x, y, 'b', linewidth = 3) 
#             plt.text(data.cor_X[i]-1, data.cor_Y[i], str(i), fontsize=15, color = 'black')
#             plt.text(coverage50index*0.98, 4, coverage50index, fontsize=10, color = 'red')  
            plt.text(data.cor_X[i]-0.2, data.cor_Y[i], str(i), fontdict = font_dict2) 

for i in range(data.nodeNum):
    for j in range(data.nodeNum):
        for k in range(data.nodeNum):
            if(solution.Y[i][j][k] == 1):
                x = [data.cor_X[i], data.cor_X[j], data.cor_X[k]] 
                y = [data.cor_Y[i], data.cor_Y[j], data.cor_Y[k]] 
                plt.plot(x, y, 'r--', linewidth = 3) 
                plt.text(data.cor_X[j]-0.2, data.cor_Y[j], str(j), fontdict = font_dict2)   
                #plt.plot(x, y, 'r--', label = "UAV", linewidth = 3) 
                    
# plt.grid(True)
plt.grid(False)  
plt.legend(loc='best', fontsize = 20) 
plt.show()   