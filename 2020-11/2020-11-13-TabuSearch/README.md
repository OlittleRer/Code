
# Tabu search for TSP 

## Introduction
禁忌搜索(Tabu Search)解决TSP问题Python的简单实现。详细讨论见[博客](https://blog.csdn.net/DCXY71/article/details/109597801)。


![在这里插入图片描述](https://img-blog.csdnimg.cn/20201210212735143.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0RDWFk3MQ==,size_16,color_FFFFFF,t_70#pic_center)

## Pseudo code
Tabu search:

> 1sBest ← s0
 2bestCandidate ← s0
 3tabuList ← []
 4tabuList.push(s0)
 5while (not stoppingCondition())
 6    sNeighborhood ← getNeighbors(bestCandidate)
 7    bestCandidate ← sNeighborhood[0]
 8    for (sCandidate in sNeighborhood)
 9        if ( (not tabuList.contains(sCandidate)) and (fitness(sCandidate) > fitness(bestCandidate)) )
10            bestCandidate ← sCandidate
11        end
12    end
13    if (fitness(bestCandidate) > fitness(sBest))
14        sBest ← bestCandidate
15    end
16    tabuList.push(bestCandidate)
17    if (tabuList.size > maxTabuSize)
18        tabuList.removeFirst()
19    end
20end
21return sBest

（from Wikipedia [https://en.wikipedia.org/wiki/Tabu_search](https://en.wikipedia.org/wiki/Tabu_search)）
## Quick start 
>python tabu_tsp.py



## Contact
Author ： 段淇耀  duanqy71@163.com

My blog:  [https://blog.csdn.net/DCXY71/article/details/109597801](https://blog.csdn.net/DCXY71/article/details/109597801)


## About us
运小筹公众号是致力于分享运筹优化(LP、MIP、NLP、随机规划、鲁棒优化)、凸优化、强化学习等研究领域的内容以及涉及到的算法的代码实现。编程语言和工具包括Java、Python、Matlab、CPLEX、Gurobi、SCIP 等。

**关注我们:  运筹小公众号**


![在这里插入图片描述](https://img-blog.csdnimg.cn/20201214000806951.png)







