from gurobipy import *
m = Model("test")
m.setParam('NonConvex', 2) #非凸模型求解参数
a  = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="a")
b  = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="b")
c  = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="c")
m1 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="m1")
m2 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="m2")
m3 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="m3")
m4 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="m4")
m5 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="m5")
m6 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="m6")
m7 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="m7")
u1 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="u1")
u2 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="u2")
u3 = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="u3")
abs_u1 = m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="abs_u1")
abs_u2 = m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="abs_u2")
abs_u3 = m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER,name="abs_u3")
lhs = m.addVar(vtype=GRB.INTEGER,name="lhs")
rhs = m.addVar(vtype=GRB.INTEGER,name="rhs")
# m.addConstr(a>=1)   #a,b,c为正整数
# m.addConstr(b>=1)
# m.addConstr(c>=1)

m.addConstr(m1 == a*a)    #a*a
m.addConstr(m2 == b*b)    #b*b
m.addConstr(m3 == c*c)    #c*c
m.addConstr(m4 == a*b)    #a*b
m.addConstr(m5 == a*c)    #a*c
m.addConstr(m6==b*c)    #b*c
m.addConstr(lhs==m1*(a+b+c)+3*m4*c+(a+b+c)*m2+m3*(a+b+c))    #左项式
m.addConstr(rhs==4*(m1*(b+c)+m2*(a+c)+(a+b)*m3+2*c*m4))        #右项式
m.addConstr(lhs==rhs)   #左右项式相等



m.addConstr(u1 == a + b)
m.addConstr(u2 == a + c)
m.addConstr(u3 == b + c)

m.addGenConstrAbs(abs_u1, u1)
m.addGenConstrAbs(abs_u2, u2)
m.addGenConstrAbs(abs_u3, u3)

m.addConstr(abs_u1 >= 0.00001)
m.addConstr(abs_u2 >= 0.00001)
m.addConstr(abs_u3 >= 0.00001)

m.setObjective(1, GRB.MINIMIZE)
m.optimize()
a1=a.x
b1=b.x
c1=c.x
print('a: ',a1)
print('b: ',b1)
print('c: ',c1)