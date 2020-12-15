
# 手把手教你python调用gurobi求解最短路问题


## Introduction

> 利用python实现迪杰斯特拉算法求解最短路问题，其中涉及到图论的一些知识。



> 效果如下

> ![](https://img-blog.csdnimg.cn/20201215163454848.png)


## Model
$$
\min  \sum_{\left( i,j \right) \in A}{c_{ij}x_{ij}}
\\
\sum_{\left( j,i \right) \in A}{x_{ij}}-\sum_{\left( i,j \right) \in A}{x_{ji}}=b_i,\forall i\in V,
\\
b_i=\begin{cases}
	-1,  if\,\,i=s,\\
	0,   if\,\,i\ne s\,\,and\,\,i\ne t,\\
	1,   if\,\,i=t,\\
\end{cases}
$$




## Quick start 
直接运行主文件即可实现功能






## Dataset Format
这里我们使用距离矩阵来表示图。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201129160124811.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3phb3d1eWluZ3NodQ==,size_16,color_FFFFFF,t_70)
copyright@https://jingyan.baidu.com/article/359911f58636ad57ff030645.html



## Contact
Your Name ：   王基光- wangjg2020@163.com

My blog:   https://blog.csdn.net/zaowuyingshu?spm=1000.2115.3001.5113


## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。


**关注我们:  运筹小公众号**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)








