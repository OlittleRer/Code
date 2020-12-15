# Simplex Algorithm

## Introduction

> 使用java实现改进的单纯形法。包括添加人工变量、进行出入基迭代等过程
> 
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020121514593363.png)

## Model
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201126200308875.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Njk5MTE3Mw==,size_16,color_FFFFFF,t_70#pic_center)

## Quick start 
> `AlgorithmProcess` ： 主函数，用于单纯形法的计算
> `MatrixOperation`： 用于定义一些单纯形法中需要用到的矩阵运算，包括求行列式的值、求余子式、求矩阵的逆、求矩阵的转置、求数组的序、求矩阵的乘法等。


## Dataset Format
人工生成的数据集，附在文件中。
>  `5个txt文件分别代表不同情况的算例`："data1"为标准唯一解算例，"data2"为存在退化解算例，"data3"为存在无穷多解算例，"data4"为存在无界解算例，"data5"为存在大于零和等于0约束的算例，"data6"为无解算例。在求解"data2"算例时，采用勃朗宁规则克服退化现象。在求解"data5"算例时，采用大M法进行计算。
>  `txt文件的数据说明：`第一堆数据依次为目标函数中变量的系数（c），以逗号隔开；第二堆数据依次为约束中变量的系数（A）；第三堆数据依次为每个式子的符号，0表示等于，-1表示小于等于，1表示大于等于；第四堆数据依次为每个式子的约束值（b）。每堆数据用空格隔开。

## Contact
曾文佳： zwj19@mails.tsinghua.edu.cn

我的CSDN:  https://blog.csdn.net/weixin_46991173?spm=1011.2124.3001.5113


## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。


**关注我们:  运筹小公众号**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)

