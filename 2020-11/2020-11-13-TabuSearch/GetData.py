'''
Description: data generation for vehicle routing problem and visualization 
Version: 1.0
Author: 71
Date: 2020-12-10 17:20:09
'''
import math,re,copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class GetData():

    def generate_locations(self,num_points,map_size,num_vehicles=1,depot=0):
        """generate number of locations randomly in a block unit
            default TSP : num_vehicles=1,depot=0
        """
        locations=[]  # locations = [(24, 3), (21, 4), (5, 1),...] 
        for i in range(num_points):
            locations.append(tuple(np.random.randint(low=0,high=map_size,size=2))) 
        class random_data():
            def __init__(self):
                self.locations = locations
                self.num_vehicles = num_vehicles
                self.depot = depot
        return random_data()

    def get_euclidean_distance_matrix(self,locations):
        """Creates callback to return distance between locations."""
        distances = {}
        for from_counter, from_node in enumerate(locations):
            distances[from_counter] = {}
            for to_counter, to_node in enumerate(locations):
                if from_counter == to_counter:
                    distances[from_counter][to_counter] = 0
                else:
                    # Euclidean distance
                    distances[from_counter][to_counter] = (int(                        
                    math.hypot((from_node[0] - to_node[0]),
                                (from_node[1] - to_node[1]))))
        return distances


    def read_solomon(self,path,customerNum=100):
        '''Description: load solomon dataset'''        
        f = open(path, 'r')
        lines = f.readlines()
        locations,demand,readyTime,dueTime,serviceTime=[],[],[],[],[]
        for count,line in enumerate(lines):
            count = count + 1
            if(count == 5):  
                line = line[:-1].strip() 
                str = re.split(r" +", line)
                vehicleNum = int(str[0])
                capacity = float(str[1])
            elif(count >= 10 and count <= 10 + customerNum):
                line = line[:-1]
                str = re.split(r" +", line)
                locations.append((float(str[2]),float(str[3])))
                demand.append(float(str[4]))
                readyTime.append(float(str[5]))
                dueTime.append(float(str[6]))
                serviceTime.append(float(str[7]))
        class Solomon_data():
            def __init__(self):
                self.locations=locations
                self.demand = demand
                self.readyTime = readyTime
                self.dueTime = dueTime
                self.serviceTime = serviceTime
                self.vehicleNum = vehicleNum
                self.capacity =capacity
        return Solomon_data()

    
    def plot_nodes(self,locations):
        ''' function to plot locations'''
        Graph = nx.DiGraph()
        nodes_name = [str(x) for x in list(range(len(locations)))]
        Graph.add_nodes_from(nodes_name)
        pos_location = {nodes_name[i]:x for i,x in enumerate(locations)}
        nodes_color_dict = ['r'] + ['gray'] * (len(locations)-1)
        nx.draw_networkx(Graph,pos_location,node_size=200,node_color=nodes_color_dict,labels=None)  
        plt.show(Graph)

    def plot_route(self,locations,route,color='k'):
        ''' function to plot locations and route'''
        Graph = nx.DiGraph()
        edge = []
        edges = []
        for i in route : 
            edge.append(i)
            if len(edge) == 2 :
                edges.append(tuple(edge))
                edge.pop(0)
        nodes_name = [x for x in list(range(len(locations)))]
        Graph.add_nodes_from(nodes_name)
        Graph.add_edges_from(edges)
        pos_location = {nodes_name[i] : x for i,x in enumerate(locations)}
        nodes_color_dict = ['r'] + ['gray'] * (len(locations)-1)
        nx.draw_networkx(Graph,pos_location,node_size=200,node_color=nodes_color_dict,edge_color=color, labels=None)  
        plt.show(Graph)


if __name__ == "__main__":
    ## generate data randomly
    data=GetData()
    random_data = data.generate_locations(num_points=10,map_size=100) 
    dismatrix = data.get_euclidean_distance_matrix(random_data.locations)
    print(dismatrix)  # get dismatrix randomly

    ## read solomon data
    path = 'E:\MIP启发式算法编辑部\Part-71\data\R101.txt'
    solomon_data = data.read_solomon(path,customerNum=9) 
    solomon_data_dismatrix = data.get_euclidean_distance_matrix(solomon_data.locations) 
    print(solomon_data_dismatrix)
    data.plot_nodes(solomon_data.locations)
    ## plot function
    # data.plot_nodes(solomon_data.locations)
    route = list(range(10))
    route.append(0)
    data.plot_route(solomon_data.locations,route)

