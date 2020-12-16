
# 手把手教你用Gurobi求解一个数学模型
> 原博客链接：https://blog.csdn.net/qq_35008055/article/details/110201571
## Introduction

> 采用python编程语言调用gurob求解器求解经典组合优化问题：带时间窗的车辆路径规划问题

求解结果（部分）：
>三个下标分别代表弧的头结点、尾结点和由哪一辆车经过这条弧。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201126205207707.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDA4MDU1,size_16,color_FFFFFF,t_70#pic_center)

## Model
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201216104035354.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDA4MDU1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201216104052400.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDA4MDU1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020121610411036.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDA4MDU1,size_16,color_FFFFFF,t_70)



## Quick start 
如何快速运行代码，或说明每一个文件如
> Data类 ： 定义Data的相关属性
> readData函数：读取数据并计算距离矩阵
> 剩余部分为gurobi建模与求解


## Dependencies
>运行代码需要导入gurobid的python包



## Dataset Format

>project中读取的数据为solomon数据集，详细信息见官网：[solomon benchmark](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/)



## Contact

Xia.Y：   - xia970201@gmail.com

My blog:  - [CSDN](https://blog.csdn.net/qq_35008055?spm=1001.2014.3001.5113)


## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。


**关注我们:  运筹小公众号**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)
