
from gurobipy import *

m = Model("pissa")
m.setParam('NonConvex', 2) #非凸模型求解参数

a  = m.addVar(lb=0, vtype=GRB.INTEGER, name="a")
b  = m.addVar(lb=0, vtype=GRB.INTEGER, name="b")
c  = m.addVar(lb=0, vtype=GRB.INTEGER, name="c")
m1 = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="m1")
m2 = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="m2")
m3 = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name="m3")

m.addConstr(a >= 1, "c1")  #a,b,c为正整数
m.addConstr(b >= 1, "c1")
m.addConstr(c >= 1, "c1")
m.addConstr(a == m1 * (b + c))
m.addConstr(b == m2 * (a + c))
m.addConstr(c == m3 * (a + b))
m.addConstr(m1 + m2 + m3 - 4 == 0)
m.setObjective(1, GRB.MINIMIZE)
m.optimize()
a1=a.x
b1=b.x
c1=c.x
print('a: ',a1)
print('b: ',b1)
print('c: ',c1)



