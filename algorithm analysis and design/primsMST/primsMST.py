# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015
@author: hwei
"""
import time
import numpy as np
from sys import maxint
from random import randint
from myHeap import minHeap

debug = False
testing = True

heap = minHeap()  ## minimum heap to sort X's adjancy verts based on their nearest distanc to X
keys = {}   ## dictionary to store vertices's nearest distance to explored set X

def heapPrimMst(graph,vertices):
    global keys,heap
    T = set()                 ## edges in MST 
    vert = list(vertices)[randint(0,len(vertices)-1)]   ##random selecting a start vert
    X = {vert}           ## insert vert to explored set X
    keys = {vert:maxint for vert in vertices-X}
    
    updateKeys(graph,vert,keys,X,heap)  ## every time add a vertice to MST, update keys and heap
    while not X == vertices:
        (v,cost,edge) = heap.getRoot()   ## get X's nearest vertice, and its cost and edge
        X.add(v)             # adding it to MST
        T.add(edge)          ## adding edge to MST                           
        updateKeys(graph,v,keys,X,heap)  ## updating keys dict and heap again
    return T

def updateKeys(graph,v,keys,X,heap):
    for (vert,cost) in graph[v]:   ## for every adjancy vert of v, and its cost
        if vert in X:   # if vert already in MST, skip
            continue
        if cost < keys[vert]:  ## if cost less than key of vert, updating it
            heap.remove(vert)
            keys[vert] = cost   ## set cost as the new key
            heap.insert((vert,cost,(v,vert)))

def naivePrimMst(graph,vertices):
    T = set()                 ## edges in MST 
    vert = list(vertices)[randint(0,len(vertices)-1)]    ##random selecting a start vert
    X = {vert}           ## verices in MST

    while X != vertices:
        e = tuple()
        cheapest = maxint
        for v in X:
           for (vert,cost) in graph[v]:
               if (vert not in X) and (cost <cheapest):
                   cheapest = cost
                   e  = (v,vert)
        T.add(e)
        X.add(e[1])
    return T
    
def inputData(filename):
    input_data_file = open(filename, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()

    lines = input_data.split('\n')

    first_line = lines[0].split()
    edge_count = int(first_line[1])
    
    graph = {}
    vertices = set()
    edges = {}
    for i in range(1, edge_count + 1):
        line = lines[i]
        [v1,v2,cost] = line.split()
        v1 = np.int32(v1)
        v2 = np.int32(v2)
        cost = np.float64(cost)
        vertices.add(v1)
        vertices.add(v2)
        edges[(v1,v2)] = cost
        edges[(v2,v1)] = cost
        if graph.has_key(v1):
            graph[v1].append((v2,cost))
        else:
            graph[v1] = [(v2,cost)]
            
        if graph.has_key(v2):
            graph[v2].append((v1,cost))
        else:
            graph[v2] = [(v1,cost)]
    return vertices, edges, graph
   
def getFileName():
    prompt = True
    while prompt:
        filename  = raw_input("Please input data file name: ")
        print "The input data file name is: %r " % filename
        p = raw_input("Does it correct (y/n)?")
        if p:
            prompt = False

    if testing:
        folder = './test/'
    else:
        folder = './data/'
    return folder+filename + '.txt'    
    
if __name__ == "__main__":

    filename = getFileName()   
    
    s_time = time.time()
    vertices,edges, graph  = inputData(filename)

    g_time = time.time()
    heapMst = heapPrimMst(graph,vertices)
    heapCost = np.sum([edges[e]  for e in heapMst])
    print "The total cost of the Heap MST is: ", heapCost
    hp_time = time.time()
    
    naiveMst = naivePrimMst(graph,vertices)
    naiveCost = np.sum([edges[e]  for e in naiveMst])
    print "The total cost of the Naive MST is: ", naiveCost
    naive_time = time.time()

    print "Graph creating time:  %s seconds ---" % (g_time - s_time)
    print "Heap Prim running time:  %s seconds ---" % (hp_time - g_time)
    print "Naive Prim running time:  %s seconds ---" % (naive_time - hp_time)
    print "Total running time:  %s seconds ---" % (time.time() - s_time)

