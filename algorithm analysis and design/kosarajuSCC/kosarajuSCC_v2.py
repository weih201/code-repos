# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015

@author: hwei
"""
import numpy as np
import zipfile
import time
debug = False
b_running = True

class myStack:
     def __init__(self):
         self.stack = []  
         
     def isEmpty(self):
         return self.size() == 0   

     def push(self, item):
         self.stack.append(item)  

     def pop(self):
         return self.stack.pop() 

     def size(self):
         return len(self.stack)  
         
     def show(self):
         print self.stack

g_leaders ={}  # record scc group key by leaders
g_f = myStack()  # record the explored sequence in the first loop

def kosarajuSCC(edges):
    global g_f,g_leaders
    
    G = edgesToGraph(edges,False)
    Grev = edgesToGraph(edges,True)
    
    print "The size of graph is: "+str(len(G))
    print "The size of grev is: "+str(len(Grev))
    
    dfs_loop(Grev,True)
    
    dfs_loop(G,False)
    
    if debug:
        print "The leaders of graph: "
        print g_leaders.keys()
        
    sccs = map(len,g_leaders.values())
    sccs.sort()
    sccs.reverse()
    print "The size of top 5 SCCs are: "
    print sccs[:5]
    
def dfs_loop(graph,b_First):
    global  g_f
    explored = {}
    
    def dfs(graph,leader,b_ft):
        e_stack = myStack()
        f_stack = myStack()
        e_stack.push(leader)
        
        while not e_stack.isEmpty():
            v = e_stack.pop()
            if not explored.has_key(v):
                explored[v] = True  # mark v explored
                f_stack.push(v)    # push v to temp explored stack
                
                if not b_ft:
                    if g_leaders.has_key(leader):
                        if debug:
                            print g_leaders[leader]
                        g_leaders[leader].append(v) 
                    else:
                        g_leaders[leader] = [v]
                if graph.has_key(v):
                    for node in graph[v]:
                        e_stack.push(node)
        if b_ft:
            while not f_stack.isEmpty():
                v = f_stack.pop()
                g_f.push(v)         # push to finish time stack

    if b_First:
        n_max = max(graph.keys())
        n_min = min(graph.keys())
        for i in range(n_max,n_min-1,-1):
            if graph.has_key(i):
                if not explored.has_key(i):
                    if debug:
                        print "Leader:"+str(i)
                    dfs(graph,i,b_First)
    else:
        while not g_f.isEmpty():
                v = g_f.pop()
                if debug:
                    print "Vert of f at: "+str(i)+" is: "+str(v)
                if not explored.has_key(v):
                    if debug:
                        print "Leader:"+str(v)
                    dfs(graph,v,b_First)
   
def edgesToGraph(edges,rev):
    graph = {}
    if not rev:
        for edge in edges:
            if graph.has_key(edge[0]):
                graph[edge[0]].append(edge[1])
            else:
                graph[edge[0]] = [edge[1]]
    else:
        for edge in edges:
            if graph.has_key(edge[1]):
                graph[edge[1]].append(edge[0])
            else:
                graph[edge[1]] = [edge[0]]
    return graph

def strToInts(intsStr):
    strlst = intsStr.split()
    return [np.int(x) for x in strlst]
    
if __name__ == "__main__":
    s_time = time.time()
    edges = []
    if b_running:  # for the required input
        with zipfile.ZipFile('./data/SCC.zip') as z:
            with z.open('SCC.txt') as f:
                for edgeStr in f:
                    edge = strToInts(edgeStr)
                    edges.append(edge) 
    else:  # testing cases
        with open('./test/61100.txt','r') as edgesStr:
            for edgeStr in edgesStr:
                edge = strToInts(edgeStr)
                edges.append(edge)
    print "Input edge number: "+str(len(edges))
    l_time = time.time()
    kosarajuSCC(edges)
    print "File loading time:  %s seconds ---" % (l_time - s_time)
    print "Total running time:  %s seconds ---" % (time.time() - s_time)

