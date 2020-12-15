'''
@author: Hsinglu Liu
@version: 1.0
@Date: 2020.11.3
'''


import math
from sympy import *

# define symbol variable
x_1 = symbols('x_1')
x_2 = symbols('x_2')

# define objective function 
fun = 2 * x_1 * x_2 + 2 * x_2 - x_1 ** 2 - 2 * x_2 ** 2
fun

# take derivative of x_1 and x_2 
grad_1 = diff(fun, x_1)
grad_2 = diff(fun, x_2)

# define parameters
MaxIter = 100  
epsilon = 0.0001

# define initial point 
x_1_value = 0.5
x_2_value = 0.5

iter_cnt = 0
current_step_size = 10000 

grad_1_value = (float)(grad_1.subs({x_1:x_1_value, x_2: x_2_value}).evalf())
grad_2_value = (float)(grad_2.subs({x_1:x_1_value, x_2: x_2_value}).evalf()) 

current_obj = fun.subs({x_1: x_1_value, x_2: x_2_value}).evalf()

print('itCnt: %2d  cur_point (%3.2f, %3.2f)   cur_Obj: %5.4f     grad_1: %5.4f     grad_2 : %5.4f     step_size : %5.4f' % (iter_cnt, x_1_value, x_2_value, current_obj, grad_1_value, grad_2_value, current_step_size)) 
    
# while (iter_cnt <= MaxIter and abs(grad_1_value) + abs(grad_2_value) >= epsilon):
while(abs(grad_1_value) + abs(grad_2_value) >= epsilon):  
    iter_cnt += 1
    # find the step size
    t = symbols('t')
    x_1_updated = x_1_value + grad_1_value * t
    x_2_updated = x_2_value + grad_2_value * t
    Fun_updated = fun.subs({x_1: x_1_updated, x_2: x_2_updated})
    grad_t = diff(Fun_updated, t)
    t_value = solve(grad_t, t)[0]  # solve grad_t == 0

    # update x_1_value and x_2_value
    grad_1_value = (float)(grad_1.subs({x_1: x_1_value, x_2: x_2_value}).evalf()) 
    grad_2_value = (float)(grad_2.subs({x_1: x_1_value, x_2: x_2_value}).evalf()) 

    x_1_value = (float)(x_1_value + t_value * grad_1_value)
    x_2_value = (float)(x_2_value + t_value * grad_2_value) 

    current_obj = fun.subs({x_1: x_1_value, x_2: x_2_value}).evalf()
    current_step_size = t_value

    print('itCnt: %2d  cur_point (%3.2f, %3.2f)   cur_Obj: %5.4f     grad_1: %5.4f     grad_2 : %5.4f     step_size : %5.4f' % (iter_cnt, x_1_value, x_2_value, current_obj, grad_1_value, grad_2_value, current_step_size)) 