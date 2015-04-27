# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015
@author: hwei
"""
import time
import numpy as np
from myHeap import minHeap

debug = False
testing = False

heap = minHeap()  ##

def clustering(cluster, graph,vertices,edgess):
    global comps,leaders,heap
    leaders,comps = compsInit(graph,vertices,edgess)

    while(len(comps)>cluster):
        ((vert1,vert2),spacing) = heap.getRoot()
        leader = merging(vert1,vert2,comps,leaders)
        s = comps[leader]
        edges = [(v1,v2) for v1 in s for v2 in s if v1!=v2]
        for edge in edges:
            heap.remove(edge)
    (edge,spacing) = heap.peepRoot()
    return spacing

def merging(v1,v2,comps,leaders):
    leader1 = leaders[v1]
    leader2 = leaders[v2]
    
    comp1 = comps[leader1]
    comp2 = comps[leader2]
    if len(comp1)<len(comp2):
        for v in comp1:
            leaders[v] = leader2
        comps[leader2] = comp1|comp2
        del comps[leader1]
        return leader2
    else:
        for v in comp2:
            leaders[v] = leader1
        comps[leader1] = comp1|comp2
        del comps[leader2]
        return leader1
    
def compsInit(graph,vertices,edgess):
    comps = {v:{v}  for v in vertices}
    leaders = {v:v for v in vertices}                 ## edges in MST 
    for edge in edges:
        heap.insert(edge)
    return leaders,comps
    
def inputData(filename):
    input_data_file = open(filename, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()

    lines = input_data.split('\n')

    verts_count = int(lines[0])
    
    graph = {}
    vertices = set()
    edges = []
    for line in lines[1:]:
        if  line.isspace() or len(line)==0:
            continue
        [v1,v2,cost] = line.split()
        v1 = np.int32(v1)
        v2 = np.int32(v2)
        cost = np.float64(cost)
        vertices.add(v1)
        vertices.add(v2)
        edges.append(((v1,v2),cost))
        if graph.has_key(v1):
            graph[v1].append((v2,cost))
        else:
            graph[v1] = [(v2,cost)]
            
        if graph.has_key(v2):
            graph[v2].append((v1,cost))
        else:
            graph[v2] = [(v1,cost)]
    return verts_count,vertices, edges, graph
   
def getFileName():
    prompt = True
    while prompt:
        filename  = raw_input("Please input data file name: ")
        print "The input data file name is: %r " % filename
        p = raw_input("Does it correct (y/n)?")
        if p=='y':
            prompt = False
    
    if testing:
        folder = './test/'
    else:
        folder = './data/'
    return folder+filename + '.txt'    
    
if __name__ == "__main__":
    
    clusterings = 4
    filename = getFileName()   
    
    s_time = time.time()
    vert_count,vertices,edges, graph  = inputData(filename)

    g_time = time.time()
    spacing = clustering(clusterings, graph,vertices,edges)
    print "The maximum spacing of input graph is: ", spacing
    cl_time = time.time()
    
#    naiveMst = naivePrimMst(graph,vertices)
#    naiveCost = np.sum([edges[e]  for e in naiveMst])
#    print "The total cost of the Naive MST is: ", naiveCost
    naive_time = time.time()

    print "Graph creating time:  %s seconds ---" % (g_time - s_time)
    print "Heap Prim running time:  %s seconds ---" % (cl_time - g_time)
    print "Naive Prim running time:  %s seconds ---" % (naive_time - cl_time)
    print "Total running time:  %s seconds ---" % (time.time() - s_time)

