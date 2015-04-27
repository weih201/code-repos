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
g_t = 0
g_f = {}

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

def kosarajuSCC(edges):
    global g_t,g_f,g_leaders
    
    G = edgesToGraph(edges,False)
    Grev = edgesToGraph(edges,True)
    
    dfs_loop(Grev,True)
    
    g_t = 0
    leaders = dfs_loop(G,False)
    sccs = map(len,leaders.values())
    sccs.sort()
    sccs.reverse()
    print "The size of top 5 SCCs are: "
    print sccs[:5]
    
def dfs_loop(graph,b_First):
    global  g_f
    leaders = {} 
    explored = {}
    
    def dfs(graph,leader,b_ft):
        global g_t
        e_stack = myStack()
        f_stack = myStack()
        e_stack.push(leader)
        
        while not e_stack.isEmpty():
            v = e_stack.pop()
            if not explored.has_key(v):
                explored[v] = True
                f_stack.push(v)
                
                if not b_ft:
                    if leaders.has_key(leader):
                        if debug:
                            print leaders[leader]
                        leaders[leader].append(v) 
                    else:
                        leaders[leader] = [v]
                if graph.has_key(v):
                    for node in graph[v]:
                        e_stack.push(node)
        if b_ft:
            while not f_stack.isEmpty():
                v = f_stack.pop()
                g_t += 1
                g_f[g_t] = v

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
        n_max = max(g_f.keys())
        n_min = min(g_f.keys())
        
        if debug:
            for key in g_f.keys():
                print "Input f("+str(key)+") =: "+str(g_f[key])
        for i in range(n_max,n_min-1,-1):
            if g_f.has_key(i):
                v = g_f[i]
                if debug:
                    print "Vert of f at: "+str(i)+" is: "+str(v)
                if not explored.has_key(v):
                    if debug:
                        print "Leader:"+str(v)
                    dfs(graph,v,b_First)
    return leaders
   
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
#     # Increase max stack size 
#    resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
#    sys.setrecursionlimit(10**6)
    s_time = time.time()

    edges = []
    if b_running:
        with zipfile.ZipFile('./data/SCC.zip') as z:
            with z.open('SCC.txt') as f:
                for edgeStr in f:
                    edge = strToInts(edgeStr)
                    edges.append(edge) 
    else:
        with open('./test/322211.txt','r') as edgesStr:
            for edgeStr in edgesStr:
                edge = strToInts(edgeStr)
                edges.append(edge)
#    print edges      
    print "Input edge number: "+str(len(edges))
    l_time = time.time()
    kosarajuSCC(edges)
    print "File loading time:  %s seconds ---" % (l_time - s_time)
    print "Total running time:  %s seconds ---" % (time.time() - s_time)

