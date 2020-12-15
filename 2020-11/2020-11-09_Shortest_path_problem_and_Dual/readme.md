# 运小筹(2020-11-9): Shortest Path Problem及其对偶问题的一些探讨(附Python调用Gurobi实现)

**关注我们:  运筹小公众号**



![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)


# Shortest Path Problem及其对偶问题的一些探讨(附Python调用Gurobi实现)

作者：刘兴禄，清华大学，清华伯克利深圳学院 (博士在读)

邮箱：hsinglul@163.com

> 原博客链接 [https://blog.csdn.net/HsinglukLiu/article/details/107834197](https://blog.csdn.net/HsinglukLiu/article/details/107834197)

## Introduction

> 本代码主要是验证Shortest path problem以及其对偶问题


文中的例子网络

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201215170957756.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70)

## Model
### Shortest path problem模型（模型1）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201215171154429.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70)

### Shortest path problem标准模型（模型2）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201215171236444.png)

### Shortest path problem的对偶问题（模型3）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201215171923187.png)


## Quick start 

 - `SPP_Gurobi.py`:是Python调用Gurobi求解模型1形式的代码
 - `SPP_Standard_form_Gurobi.py`：是Python调用Gurobi求解模型2形式的代码
 - `SPP_Dual.py`：是Python调用Gurobi求解模型3形式的代码


## Dependencies

> gurobi
> numpy
> pandas


## Dataset Format
Solomon VRP benchmark instance
下载地址[https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/)

```python
Nodes = ['s', 'a', 'b', 'c', 't'] 

Arcs = {('s','a'): 5 
        ,('s','b'): 8
        ,('a','c'): 2
        ,('b','a'): -10
        ,('c','b'): 3
        ,('b','t'): 4
        ,('c','t'): 3
       }
Arcs
```



## Contact
Your Name ：刘兴禄   hsinglul@163.com

My blog:   [https://blog.csdn.net/HsinglukLiu?spm=1010.2135.3001.5113](https://blog.csdn.net/HsinglukLiu?spm=1010.2135.3001.5113)


## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。


**关注我们:  运筹小公众号**



![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)
