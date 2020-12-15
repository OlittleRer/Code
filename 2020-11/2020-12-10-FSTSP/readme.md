@[TOC] 
# 无人机与卡车联合配送-论文代码复现

> 原博客链接 [https://blog.csdn.net/HsinglukLiu/article/details/107871295](https://blog.csdn.net/HsinglukLiu/article/details/107871295)

## Introduction

> 本代码主要是复现了2015年发表在`Transportation Research Part C: Emerging Technologies`上的关于无人机与卡车联合配送的文章中的模型部分的求解器求解代码。论文题目为`The flying sidekick traveling salesman problem: Optimization of drone-assisted parcel delivery`.

代码求解结果可视化效果如图

> 例如：
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/2020121514204017.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70)


## Model
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201215152748669.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201215152805509.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0hzaW5nbHVrTGl1,size_16,color_FFFFFF,t_70)


> 
> $$\begin{aligned}
\min & \quad t_{c+1}  
\\
\text { s.t. } & \sum_{i \in N_{0} \atop i \neq j} x_{i j}+\sum_{i \in N_{0}} \sum_{k \in N_{+} \atop i \neq j} y_{i j k}=1,   \quad \forall j \in C
\\
&\sum_{j \in N_{+}} x_{0 j}=1,   
\\ 
&\sum_{i \in N_{0}} x_{i, c+1}=1 ,  
\\ 
&u_{i}-u_{j}+1 \leq (c+2)\left(1-x_{i j}\right),   \quad \forall i \in C, j \in\left\{N_{+}: j \neq i\right\} 
\\ 
&\sum_{i \in N_{0}} x_{i j}=\sum_{k \in N_{+} \atop i \neq j} x_{j k},   \quad \forall j \in C
\\
&\sum_{j \in C} \sum_{k \in N_{t} \atop j \neq i(j, j) \in P} y_{i j k} \leq 1,   \quad \forall i \in N_{0}
\\
&\sum_{i \in N_{0} \atop i \neq k} \sum_{j \in C \atop i \neq i, j, k\rangle \in P} y_{i j k} \leq 1,   \quad \forall k \in N_{+}
\\
&2 y_{i j k} \leq \sum_{h \in N_{0} \atop h \neq i} x_{h i}+\sum_{l \in C \atop l \neq k} x_{l k},   \quad 
\\
& \hspace{2cm} \forall i \in C, j \in\{C: j \neq i\}, k \in\left\{N_{+}:\langle i, j, k\rangle \in P\right\}
\\
&y_{0 j k} \leq \sum_{h \in N_{0} \atop h \neq k} x_{h k},   \quad \forall j \in C, k \in\left\{N_{+}:\langle 0, j, k\rangle \in P\right\}
\\
&u_{k}-u_{i} \geq 1-(c+2)\left(1-\sum_{j \in C} y_{i j k}\right),   \quad     
\\
&\hspace{2cm}\forall i \in C, k \in\left\{N_{+}: k \neq i\right\} 
\\ 
&t_{i}^{\prime} \geq t_{i}-M\left(1-\sum_{j \in C} \sum_{k \in N_{+} \atop j \neq i} y_{i j k}\right),   \quad \forall i \in C
\\
&t_{i}^{\prime} \leq t_{i}+M\left(1-\sum_{j \in C \atop j \neq i} \sum_{k \in N_{+} \atop\langle i, j\rangle \in P} y_{i j k}\right),   \quad \forall i \in C
\\
&t_{k}^{\prime} \geq t_{k}-M\left(1-\sum_{i \in N_{0}} \sum_{j \in C \atop i \neq k} y_{i j k}\right),   \quad \forall k \in N_{+}
\\
&t_{k}^{\prime} \leq t_{k}+M\left(1-\sum_{i \in N_{0} \atop i \neq k(i j, k) \in P} y_{i j k}\right),   \quad \forall k \in N_{+}
\\
&t_{k} \geq t_{h}+\tau_{h k}+s_{L}\left(\sum_{l \in C} \sum_{m \in N_{+} \atop l \neq k} y_{k l m}\right)+s_{R}\left(\sum_{i \in N_{0}} \sum_{j \in C} y_{i j k}\right)-M\left(1-x_{h k}\right),    
\\
&\hspace{2cm}\forall h \in N_{0}, k \in\left\{N_{+}: k \neq h\right\}
\\
&t_{j}^{\prime} \geq t_{i}^{\prime}+\tau_{i j}^{\prime}-M\left(1-\sum_{k \in N_{+} \atop\langle i, j, k) \in P} y_{i j k}\right) \quad \forall j \in C^{\prime}, i \in\left\{N_{0}: i \neq j\right\}
\\
&t_{k}^{\prime} \geq t_{j}^{\prime}+\tau_{j k}^{\prime}+s_{R}-M\left(1-\sum_{i \in N_{0} \atop\langle i, j, k \in P} y_{i j k}\right) \quad    
\\
&\hspace{2cm}\forall j \in C^{\prime}, k \in\left\{N_{+}: k \neq j\right\}
\\
&t_{k}^{\prime}-\left(t_{j}^{\prime}-\tau_{i j}^{\prime}\right) \leq e+M\left(1-y_{i j k}\right) \quad   
\\
&\hspace{2cm}\forall k \in N_{+}, j \in\{C: j \neq k\}, i \in\left\{N_{0}:\langle i, j, k\rangle \in P\right\}
\\
&u_{i}-u_{j} \geq 1-(c+2) p_{i j} \forall i \in C, j \in\{C: j \neq i\} 
\\ 
&u_{i}-u_{j} \leq-1+(c+2)\left(1-p_{i j}\right) \forall i \in C, j \in\{C: j \neq i\}
 \\ 
&p_{i j}+p_{j i}=1 \quad \forall i \in C, j \in\{C: j \neq i\}
\\
&t_{l}^{\prime} \geq t_{k}^{\prime}-M(3-\sum_{j \in C} y_{i j k}-\sum_{m \in C} \sum_{n \in N_{+} \atop\{i j, k \in P} y_{l m n}-p_{i l}    
\\
&\hspace{2cm} \forall i \in N_{0}, k \in\left\{N_{+}: k \neq i\right\}, l \in\{C: l \neq i, l \neq k\}
\\
&t_{0}=0 ,  
\\
&t_{0}^{\prime}=0 ,  
\\ 
&p_{0 j}=1,   \quad \forall j \in C 
\\ 
&x_{i j} \in\{0,1\},   \quad \forall i \in N_{0}, j \in\left\{N_{+}: j \neq i\right\} 
\\ 
&y_{i j k} \in\{0,1\} ,  \quad \forall i \in N_{0}, j \in\{C: j \neq i\}, k \in\left\{N_{+}:\langle i, j, k\rangle \in P\right\} 
\\ 
&1 \leq u_{i} \leq c+2,   \quad \forall i \in N_{+}
\\
&t_{i} \geq 0,   \quad \forall i \in N \\ &t_{i}^{\prime} \geq 0 \quad \forall i \in N 
\\ 
&p_{i j} \in\{0,1\},   \quad \forall i \in N_{0}, j \in\{C: j \neq i\}		
\end{aligned}
$$

## Quick start 
> `Data`类：存储算例数据
> `Solution`类：提取问题最优解的类
> 其中函数
> `getSolution(self, data, model)` 用于提取最优解的信息

> `readData(data, path, customerNum)` : 读取文件路径`path`中的数据，客户点的个数设置为`customerNum`个，返回一个`data`类型的实例。
> 

## Dependencies

> gurobi
> numpy
> math
> re
> matplotlib
> pandas


## Dataset Format
Solomon VRP benchmark instance
下载地址[https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/)

```python
C101

VEHICLE
NUMBER     CAPACITY
  25         200

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE   TIME
 
    0      40         50          0          0       1236          0   
    1      45         68         10        912        967         90   
    2      45         70         30        825        870         90   
    3      42         66         10         65        146         90   
    4      42         68         10        727        782         90   
    5      42         65         10         15         67         90   
    6      40         69         20        621        702         90   
    7      40         66         20        170        225         90   
    8      38         68         20        255        324         90   
    9      38         70         10        534        605         90   
   10      35         66         10        357        410         90   
   11      35         69         10        448        505         90   
   12      25         85         20        652        721         90   
   13      22         75         30         30         92         90   
   14      22         85         10        567        620         90   
   15      20         80         40        384        429         90   
   16      20         85         40        475        528         90   
   17      18         75         20         99        148         90   
   18      15         75         20        179        254         90   
   19      15         80         10        278        345         90   
   20      30         50         10         10         73         90   
   21      30         52         20        914        965         90   
   22      28         52         20        812        883         90   
   23      28         55         10        732        777         90   
   24      25         50         10         65        144         90   
   25      25         52         40        169        224         90   
   26      25         55         10        622        701         90   
   27      23         52         10        261        316         90   
   28      23         55         20        546        593         90   
   29      20         50         10        358        405         90   
   30      20         55         10        449        504         90   
   31      10         35         20        200        237         90   
   32      10         40         30         31        100         90   
   33       8         40         40         87        158         90   
   34       8         45         20        751        816         90   
   35       5         35         10        283        344         90   
   36       5         45         10        665        716         90   
   37       2         40         20        383        434         90   
   38       0         40         30        479        522         90   
   39       0         45         20        567        624         90   
   40      35         30         10        264        321         90   
   41      35         32         10        166        235         90   
   42      33         32         20         68        149         90   
   43      33         35         10         16         80         90   
   44      32         30         10        359        412         90   
   45      30         30         10        541        600         90   
   46      30         32         30        448        509         90   
   47      30         35         10       1054       1127         90   
   48      28         30         10        632        693         90   
   49      28         35         10       1001       1066         90   
   50      26         32         10        815        880         90   
   51      25         30         10        725        786         90   
   52      25         35         10        912        969         90   
   53      44          5         20        286        347         90   
   54      42         10         40        186        257         90   
   55      42         15         10         95        158         90   
   56      40          5         30        385        436         90   
   57      40         15         40         35         87         90   
   58      38          5         30        471        534         90   
   59      38         15         10        651        740         90   
   60      35          5         20        562        629         90   
   61      50         30         10        531        610         90   
   62      50         35         20        262        317         90   
   63      50         40         50        171        218         90   
   64      48         30         10        632        693         90   
   65      48         40         10         76        129         90   
   66      47         35         10        826        875         90   
   67      47         40         10         12         77         90   
   68      45         30         10        734        777         90   
   69      45         35         10        916        969         90   
   70      95         30         30        387        456         90   
   71      95         35         20        293        360         90   
   72      53         30         10        450        505         90   
   73      92         30         10        478        551         90   
   74      53         35         50        353        412         90   
   75      45         65         20        997       1068         90   
   76      90         35         10        203        260         90   
   77      88         30         10        574        643         90   
   78      88         35         20        109        170         90   
   79      87         30         10        668        731         90   
   80      85         25         10        769        820         90   
   81      85         35         30         47        124         90   
   82      75         55         20        369        420         90   
   83      72         55         10        265        338         90   
   84      70         58         20        458        523         90   
   85      68         60         30        555        612         90   
   86      66         55         10        173        238         90   
   87      65         55         20         85        144         90   
   88      65         60         30        645        708         90   
   89      63         58         10        737        802         90   
   90      60         55         10         20         84         90   
   91      60         60         10        836        889         90   
   92      67         85         20        368        441         90   
   93      65         85         40        475        518         90   
   94      65         82         10        285        336         90   
   95      62         80         30        196        239         90   
   96      60         80         10         95        156         90   
   97      60         85         30        561        622         90   
   98      58         75         20         30         84         90   
   99      55         80         10        743        820         90   
  100      55         85         20        647        726         90   

```


solomon相关数据集、最优解等详细信息见官网：[solomon benchmark](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/)



## Contact
Your Name ：  hsinglul@163.com

My blog:   [https://blog.csdn.net/HsinglukLiu?spm=1010.2135.3001.5113](https://blog.csdn.net/HsinglukLiu?spm=1010.2135.3001.5113)


## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。


**关注我们:  运筹小公众号**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)







