
# Java调用cplex求解运输问题
> 原博客链接：https://blog.csdn.net/qq_35008055/article/details/109880741

运行结果：
![在这里插入图片描述](https://img-blog.csdnimg.cn/202012152212076.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDA4MDU1,size_16,color_FFFFFF,t_70)
## Introduction
>采用Java编程语言调用cplex求解器求解了经典线性规划问题：运输问题。

## Model
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201120222111607.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDA4MDU1,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020121522594958.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDA4MDU1,size_16,color_FFFFFF,t_70)



## Quick start 

> transportation_node.java：定义节点
> transportation_relation.java：定义节点间的关系
> Readfile.java：读取文件类
> model_transportation.java：在cplex中建立运输问题模型
> Main.java：主函数


## Dependencies
> 需要在project中导入cplex.jar

## Contact
Xia.Y：   - xia970201@gmail.com

My blog:  - [CSDN](https://blog.csdn.net/qq_35008055?spm=1001.2014.3001.5113)

## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。


**关注我们:  运筹小公众号**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)

