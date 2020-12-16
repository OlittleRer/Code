from gurobipy import *

class Data:
    customerNum = 0
    nodeNum     = 0
    vehicleNum  = 0
    capacity    = 0
    cor_X       = []
    cor_Y       = []
    demand      = []
    serviceTime = []
    readyTime   = []
    dueTime     = []
    disMatrix   = [[]]   # 读取数据

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
        if (count == 5):
            line = line[:-1].strip()
            str = re.split(r" +", line)
            data.vehicleNum = int(str[0])
            data.capacity = float(str[1])
        elif (count >= 10 and count <= 10 + customerNum):
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
    # data.disMatrix = [[0] * nodeNum] * nodeNum]; 这个是浅拷贝，容易重复
    for i in range(0, data.nodeNum):
        for j in range(0, data.nodeNum):
            temp = (data.cor_X[i] - data.cor_X[j]) ** 2 + (data.cor_Y[i] - data.cor_Y[j]) ** 2
            data.disMatrix[i][j] = math.sqrt(temp)
            #             if(i == j):
            #                 data.disMatrix[i][j] = 0;
            # print("%6.2f" % (math.sqrt(temp)), end = " ");
            temp = 0

    return data


def printData(data, customerNum):
    print("下面打印数据\n")
    print("vehicle number = %4d" % data.vehicleNum)
    print("vehicle capacity = %4d" % data.capacity)
    for i in range(len(data.demand)):
        print('{0}\t{1}\t{2}\t{3}'.format(data.demand[i], data.readyTime[i], data.dueTime[i], data.serviceTime[i]))

    print("-------距离矩阵-------\n")
    for i in range(data.nodeNum):
        for j in range(data.nodeNum):
            # print("%d   %d" % (i, j));
            print("%6.2f" % (data.disMatrix[i][j]), end=" ")
        print()


# # Read Data

# In[12]:


# reading data
data = Data()
# path = r'C:\Users\hsingluLiu\eclipse-workspace\PythonCallGurobi_Applications\VRPTW\c101.txt'
path = 'c101.txt'

# path = r'C:\Users\hsingluLiu\eclipse-workspace\PythonCallGurobi_Applications\VRPTW\R101.txt';
customerNum = 4
readData(data, path, customerNum)
data.vehicleNum = 2
printData(data, customerNum)

# # Build and solve VRPTW

# In[13]:

BigM = 100000

model = Model('VRPTW')

x = {}
s = {}

#定义决策变量
for i in range(data.nodeNum):
    for k in range(data.vehicleNum):
        name = 's_' + str(i) + '_' + str(k)
        s[i,k] = model.addVar(0
                              , 1500
                              , vtype= GRB.CONTINUOUS
                              , name= name)
        for j in range(data.nodeNum):
            if(i != j):
                name = 'x_' + str(i) + '_' + str(j) + '_' + str(k)
                x[i,j,k] = model.addVar(0
                                        , 1
                                        , vtype= GRB.BINARY
                                        , name= name)

#更新模型
model.update()

#定义目标函数
obj = LinExpr(0)
for i in range(data.nodeNum):
    for k in range(data.vehicleNum):
        for j in range(data.nodeNum):
            if(i != j):
                obj.addTerms(data.disMatrix[i][j], x[i,j,k])
model.setObjective(obj, GRB.MINIMIZE)



#定义约束一
for k in range(data.vehicleNum):
    lhs = LinExpr(0)
    for j in range(data.nodeNum):
        if(j != 0):
            lhs.addTerms(1, x[0,j,k])
    model.addConstr(lhs == 1, name= 'vehicle_depart_' + str(k))

# for i in range(1, data.nodeNum - 1):
#     lhs = LinExpr(0)
#     for j in range(data.nodeNum):
#         if(i != j):
#             for k in range(data.vehicleNum):
#                 lhs.addTerms(1, x[i,j,k])
#     for h in range(data.nodeNum):
#         if (i != h):
#             for k in range(data.vehicleNum):
#                 lhs.addTerms(-1, x[h, i, k])
#     model.addConstr(lhs == 0, name= 'flow_conservation_' + str(i))
#定义约束二
for k in range(data.vehicleNum):
    for h in range(1, data.nodeNum - 1):
        expr1 = LinExpr(0)
        expr2 = LinExpr(0)
        for i in range(data.nodeNum):
            if (h != i):
                expr1.addTerms(1, x[i,h,k])

        for j in range(data.nodeNum):
            if (h != j):
                expr2.addTerms(1, x[h,j,k])

        model.addConstr(expr1 == expr2, name= 'flow_conservation_' + str(i))
        expr1.clear()
        expr2.clear()

#定义约束三
for k in range(data.vehicleNum):
    lhs = LinExpr(0)
    for j in range(data.nodeNum - 1):
        if(j != 0):
            lhs.addTerms(1, x[j, data.nodeNum-1, k])
    model.addConstr(lhs == 1, name= 'vehicle_depart_' + str(k))

#定义约束四
for i in range(1, data.nodeNum - 1):
    lhs = LinExpr(0)
    for k in range(data.vehicleNum):
        for j in range(1, data.nodeNum):
            if(i != j):
                lhs.addTerms(1, x[i,j,k])
    model.addConstr(lhs == 1, name= 'customer_visit_' + str(i))

for k in range(data.vehicleNum):
    model.addConstr(x[0, data.nodeNum - 1, k] == 0)

#定义约束五
#time windows
for k in range(data.vehicleNum):
    for i in range(data.nodeNum):
        for j in range(data.nodeNum):
            if(i != j):
                model.addConstr(s[i,k] + data.disMatrix[i][j] + data.serviceTime[i] - s[j,k]
                                - BigM + BigM * x[i,j,k] <= 0 , name= 'time_windows_')

#定义约束六
for i in range(1,data.nodeNum-1):
    for k in range(data.vehicleNum):
        model.addConstr(data.readyTime[i] <= s[i,k], name= 'ready_time')
        model.addConstr(s[i,k] <= data.dueTime[i], name= 'due_time')

#定义约束七
for k in range(data.vehicleNum):
    lhs = LinExpr(0)
    for i in range(1, data.nodeNum - 1):
        for j in range(data.nodeNum):
            if(i != j):
                lhs.addTerms(data.demand[i], x[i,j,k])
    model.addConstr(lhs <= data.capacity, name= 'capacity_vehicle' + str(k))

#导出模型
model.write('VRPTW1.lp')
#求解
model.optimize()

#打印结果
print("\n\n-----optimal value-----")
print(model.ObjVal)

for key in x.keys():
    if(x[key].x > 0 ):
        print(x[key].VarName + ' = ', x[key].x)












