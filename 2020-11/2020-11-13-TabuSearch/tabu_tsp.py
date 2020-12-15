from itertools import combinations
import os,sys,copy
import numpy as np
import time
import matplotlib.pyplot as plt
from GetData import *
from tqdm import tqdm

class Tabu():
    def __init__(self,disMatrix,max_iters=50,maxTabuSize=10):
        """parameters definition"""
        self.disMatrix = disMatrix
        self.maxTabuSize = maxTabuSize
        self.max_iters = max_iters
        self.tabu_list=[]

    def get_route_distance(self,route):
        '''
        Description: function to calculate total distance of a route. evaluate function.
        parameters: route : list
        return : total distance : folat
        '''        
        routes = [0] + route + [0]    # add the start and end point 
        total_distance = 0
        for i,n in enumerate(routes):
            if i != 0 :
                total_distance = total_distance +  self.disMatrix[last_pos][n] 
            last_pos = n
        return total_distance

    def exchange(self,s1,s2,arr):
        """
        function to Swap positions of two elements in an arr
        Args: int,int,list
            s1 : target 1 
            s2 : target 2  
            arr : target array 
        Ouput: list
            current_list : target array 
        """
        current_list = copy.deepcopy(arr)
        index1 , index2 = current_list.index(s1) , current_list.index(s2)  # get index
        current_list[index1], current_list[index2]= arr[index2] , arr[index1]
        return current_list

    def generate_initial_solution(self,num=10,mode='greedy'):
        """
        function to get the initial solution,there two different way to generate route_init.
        Args: 
            num :  int
                the number of points 
            mode : string
                "greedy" : advance step by choosing optimal one 
                "random" : randomly generate a series number
        Ouput: list
            s_init : initial solution route_init
        """
        if mode == 'greedy':
            route_init=[0]
            for i in range(num):
                best_distance = 10000000
                for j in range(num+1):
                    if self.disMatrix[i][j] < best_distance and j not in route_init:  
                        best_distance = self.disMatrix[i][j]
                        best_candidate = j
                route_init.append(best_candidate)
            route_init.remove(0)
                            
        if mode == 'random':
            route_init = np.arange(1,num+1)  #init solution from 1 to num
            np.random.shuffle(route_init)  #shuffle the list randomly

        return list(route_init)

    def tabu_search(self,s_init):   
        """tabu search"""
        s_best = s_init 
        bestCandidate = copy.deepcopy(s_best)
        routes , temp_tabu = [] , []   # init
        routes.append(s_best)
        while(self.max_iters):
            self.max_iters -= 1 # Number of iterations
            neighbors = copy.deepcopy(s_best)
            for s in combinations(neighbors, 2):   
                sCandidate = self.exchange(s[0],s[1],neighbors)  # exchange number to generate candidates
                if s not in self.tabu_list and self.get_route_distance(sCandidate) < self.get_route_distance(bestCandidate):
                    bestCandidate = sCandidate
                    temp_tabu = s                           
            if self.get_route_distance(bestCandidate) < self.get_route_distance(s_best): # record the best solution 
                s_best = bestCandidate
            if  temp_tabu not in self.tabu_list:
                self.tabu_list.append(temp_tabu)
            if len(self.tabu_list) > self.maxTabuSize :
                self.tabu_list.pop(0)
            routes.append(bestCandidate)
        return s_best, routes

if __name__ == "__main__":
    np.random.seed(2020)
    customerNum = 10  # 定义多少个点
    data=GetData()
    tsp_data = data.generate_locations(num_points=customerNum+1,map_size=100)  #在100*100的图中，随机生成位置，customerNum+1 多一个depot点
    dismatrix = data.get_euclidean_distance_matrix(tsp_data.locations)
    # data.plot_nodes(tsp_data.locations)
    """ Tabu : 
        disMatrix : the distance matrix from 0 to X , 0 represernt starting and stopping point。 
        for example:   disMatrix = [[0,3,4,...
        							 1,0,5,...
        							 3,5,0,...]]
       that means the distance from 0 to 0 is 0, from 0 to 1 is 3,... from 1 to 3 is 5....		
        max_iters : maximum iterations 
        maxTabuSize : maximum iterations 
    """
    tsp = Tabu(disMatrix=dismatrix ,max_iters=20,maxTabuSize=10)   # 设置参数
	# two different way to generate initial solution
	# num : the number of points   
    s_init = tsp.generate_initial_solution(num=customerNum,mode='greedy') # mode = "greedy"  or "random"
    print('init route : ' , s_init)
    print('init distance : ' , tsp.get_route_distance(s_init))

    start = time.time()
    best_route , routes = tsp.tabu_search(s_init)     # tabu search
    end = time.time()

    print('best route : ' , best_route)
    print('best best_distance : ' , tsp.get_route_distance(best_route))
    print('the time cost : ',end - start )

    # plot the result changes with iterations
    results=[]
    for i in routes:
        results.append(tsp.get_route_distance(i))    
    plt.plot(np.arange(len(results)) , results)
    plt.show()
    # plot the route
    data.plot_route(tsp_data.locations,[0]+best_route+[0])
