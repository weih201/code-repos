# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015

@author: hwei
"""
import numpy as np
import random as rnd

def kargerMinCut(vertices):
    edges = vertToEdges(vertices)
    
    print "Input vertices size: "+str(len(vertices))
    print "Initial edges length: "+str(len(edges))
    
    minCut = len(edges)
    minCutEdges = []
    for i in np.arange(200):
        (cut,cutEdges) = contraction(edges)
        if cut<minCut:
            minCut = cut
            minCutEdges = cutEdges
            
    return (minCut,minCutEdges)

def contraction(edges):
    vertices = set()
    for (u,v) in edges:
        vertices.add(u)
        vertices.add(v)
 
    if len(vertices)>2:
        newEdges = []   
        (u,v) = edges[rnd.randint(0,len(edges)-1)]
        for (ui,vi) in edges:
            if ui == v:
                newEdges.append((u,vi))
            elif vi==v:
                newEdges.append((ui,u))
            else:
                newEdges.append((ui,vi))
        return contraction(removeSelfLoop(newEdges)) 
    else:
        return (len(edges),edges)
   
def vertToEdges(vertices):
    edges = []
    for vertice in vertices:
        pvertices = vertice[1:]
        hlst = [vertice[0]]*len(pvertices)
        edges.extend(zip(hlst,pvertices))
    return removeDupEdges(edges)

def removeDupEdges(edges):
    uniedges =[]
    [uniedges.append((u,v)) for (u,v) in edges if ((not (u,v) in uniedges) and (not (v,u) in uniedges)) ]
    return uniedges

def removeSelfLoop(edges):
    uniedges =[]
    [uniedges.append((u,v)) for (u,v) in edges if (u<>v) ]
    return uniedges

def strToInts(intsStr):
    strlst = intsStr.split()
    return [np.int(x) for x in strlst]
    
if __name__ == "__main__":
     
    test1 = [[1, 2, 3, 4, 5], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3, 8],
             [5, 1, 6, 7 ,8], [6, 7, 8 ,5], [7, 8, 5, 6], [8 ,4, 6, 5, 7]]  # exp 2
    test2 = [[1, 19, 15, 36, 23, 18, 39 ], [2, 36, 23, 4, 18, 26, 9], [3, 35, 6, 16, 11], [4, 23, 2, 18, 24],
            [5, 14, 8, 29, 21], [6, 34, 35, 3, 16], [7, 30, 33, 38, 28], [8, 12, 14, 5, 29, 31],
        [9, 39, 13, 20, 10, 17, 2],[10, 9, 20, 12, 14, 29],[11, 3, 16, 30, 33, 26],
        [12, 20, 10, 14, 8],[13, 24, 39, 9, 20],[14, 10, 12, 8, 5],
        [15, 26, 19, 1, 36],[16, 6, 3, 11, 30, 17, 35, 32],[17, 38, 28, 32, 40, 9, 16],
        [18, 2, 4, 24, 39, 1],[19, 27, 26, 15, 1],[20, 13, 9, 10, 12],
        [21, 5, 29, 25, 37],[22, 32, 40, 34, 35],[23, 1, 36, 2, 4],
        [24, 4, 18, 39, 13],[25, 29, 21, 37, 31],[26, 31, 27, 19, 15, 11, 2],
        [27, 37, 31, 26, 19, 29],[28, 7, 38, 17, 32],[29, 8, 5, 21, 25, 10, 27],
        [30, 16, 11, 33, 7, 37],[31, 25, 37, 27, 26, 8],[32, 28, 17, 40, 22, 16],
        [33, 11, 30, 7, 38],[34, 40, 22, 35, 6],[35, 22, 34, 6, 3, 16],
      [36, 15, 1, 23, 2],[37, 21, 25, 31, 27, 30],[38, 33, 7, 28, 17, 40],
        [39, 18, 24, 13, 9, 1],[40, 17, 32, 22, 34, 38 ]]      # expect: 3

    with open("../data/kargerMinCut.txt", "r") as verticesStr:
        vertices = []
        for verticeStr in verticesStr:
            vertice = strToInts(verticeStr)
            vertices.append(vertice) 
#    print vertices
    (minCut,cutEdges) = kargerMinCut(vertices)
    print 'The minimum cut of the input graph is :' + str(minCut)
    print 'The edges cross the cut are: '
    print cutEdges