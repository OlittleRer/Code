
@[TOC]

# Python实现最速下降法(The steepest descent method)详细案例

> 原博客链接 [https://blog.csdn.net/HsinglukLiu/article/details/109524062](https://blog.csdn.net/HsinglukLiu/article/details/109524062)

## Introduction

> 本代码主要是介绍Python实现最速下降法(The steepest descent method)及其详细案例

代码求解结果可视化效果如图

> 例如：
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20201215173134647.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70)




## Algorithm

> 本文中的课件来自清华大学深圳国际研究生院，物流与交通学部张灿荣教授《高级运筹学》课程。
> 
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020121517324338.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70)


## Quick start 
本代码主要涉及python的符号函数包 	`sympy`，简要介绍如下，具体介绍见【运小筹】公众号推文

`优化|最速下降法：详细案例+Python实现`

[https://mp.weixin.qq.com/s/lS5BhxnZcVoS991XTb6MmQ](https://mp.weixin.qq.com/s/lS5BhxnZcVoS991XTb6MmQ)


#### 构建符号变量和符号函数
```python
from sympy import * 
x_1 = symbols('x_1')
x_2 = symbols('x_2') 
              
fun = 2 * x_1 * x_2 + 2 * x_2 - x_1**2 - 2 * x_2**2
fun  
```
这个是用来构造两个符号变量$x_1, x_2$，就像代数中用字母代替变量一样。然后可以定义出我们的函数
$$
\begin{aligned}
f(x_1,x_2)=&2x_1x_2 +2x_2-x_1^2-2x_2^2 ,
\end{aligned}
$$

`jupyter notebook`中的显示效果是这样的

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201106024350479.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70#pic_center)
可以看到`jupyter notebook`中直接就显示出了数学公式格式的形式，这是因为`jupyter notebook`中内嵌了`LaTeX`相关支持包的缘故。总之这样可视化就非常不错。


## Dependencies

> sympy
> math 


## Dataset Format



## Contact
Your Name ： 刘兴禄  hsinglul@163.com

My blog:   [https://blog.csdn.net/HsinglukLiu?spm=1010.2135.3001.5113](https://blog.csdn.net/HsinglukLiu?spm=1010.2135.3001.5113)


## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。


**关注我们:  运筹小公众号**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)
