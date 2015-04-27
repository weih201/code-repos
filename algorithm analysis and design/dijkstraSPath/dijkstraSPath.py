# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015

@author: hwei
"""
from myHeap import minHeap
from sys import maxint
import time
debug = False
testing = False

NOPATH = 1000000
heap = minHeap()  ## minimum heap to sort X's adjancy verts based on their nearest distanc to X
graph = {}

def shortestDist(input_data,start,end):
    global graph
    lines = input_data.split('\n')

    graphLines=[]
    for line in lines:
        graphLines.append(line.split())
       
    graph,vertices = linesToGraph(graphLines)
#    return  heapDijkstra(graph,vertices,start,end)
    return naiveDijkstra(graph,start,end)
    
def heapDijkstra(graph,vertices,start,end):
    global heap
    paths = {}   ## dist dict from source
    X=set()   # explored vertices set
    X.add(start)   # add source to explored
    paths = {vert:maxint for vert in vertices-X}  # Init distance to maxint
    paths[start] = 0
    
    updateDist(graph,start,paths,X,heap)  ## every time explored a, update paths and heap
    while not X == vertices:
        (v,cost) = heap.getRoot()   ## get X's nearest vertice, and its cost 
        X.add(v)             # addig to explored vertices set
        updateDist(graph,v,paths,X,heap)  ## updating paths dict and heap again
    return paths[end]

def updateDist(graph,v,paths,X,heap):
    if not v in graph:  ## v doesn't have out-edges
        return 
    for (vert,cost) in graph[v]:   ## for every adjancy vert of v, and its cost
        if vert in X:   # if vert is already explored, skip
            continue
        if cost+paths[v] < paths[vert]:  ##if the distance via v is less than vert's original dist, updating it
            heap.remove(vert)
            paths[vert] = cost+paths[v]   ## set new distanc as the shortest distance to source so far
            heap.insert((vert,cost+paths[v]))


def naiveDijkstra(graph,start,end):
    paths = {}
    X=list()
    X.append(start)
    paths[start] = 0
    while True:
        (v,l) = naiveMin(graph,X,paths)
        X.append(v)
        paths[v] = l
        if v==end:
            break
    return paths[end]

def naiveMin(graph,X,paths):
    lmin = NOPATH
    wmin = 0
    for v in X:
       for (w,l) in graph[v]:
           if (w not in X) and ( (l+paths[v]) <lmin):
               lmin = l+paths[v]
               wmin = w
    return wmin,lmin
    
def linesToGraph(gLines):
    graph = {}
    vertices = set()
    for line in gLines:
        if len(line)==0:
            continue
        key = int(line[0])
        vertices.add(key)
        val = map(strToTuple,line[1:])
        graph[key] = val
        for v,dist in val:
            vertices.add(v)
    return graph,vertices
     
def strToTuple(intsStr):
    strlst = intsStr.split(',')
    return int(strlst[0]),int(strlst[1])
    
import sys
if __name__ == "__main__":
    if len(sys.argv) > 1:
        s_time = time.time()
        file_location = sys.argv[1].strip()
        start = int(sys.argv[2].strip())
        end = int(sys.argv[3].strip())
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        ld_time = time.time()
        mindist =  shortestDist(input_data,start,end)
        
        print "The shortest distance from %s to %s is: %d"%(start,end,mindist)
        print "File loading time:  %s seconds ---" % (ld_time - s_time)
        print "Total running time:  %s seconds ---" % (time.time() - s_time)
    else:
        print 'This test requires an input file.  Please select one from' \
        'the data directory. (i.e. python dijkstraSPath.py ./data/g1.txt  start end)'

