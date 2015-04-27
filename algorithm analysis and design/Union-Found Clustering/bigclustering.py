# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015
@author: hwei
"""
import time
from bitarray import bitarray

testing = False

hammingcode = set()
b_nodes= bitarray()


def naiveClustering(graph):
    comps={}
    avail_verts = [True for i in graph]
    while sum(avail_verts)>0:
        leader = -1
        leadercode =-1
        for v in range(len(graph)):
            if avail_verts[v]:  
                if leader<0:
                    leader= v
                    comps[v] = {v}
                    leadercode = graph[v]
                    avail_verts[v] = False
                else:
                    code = graph[v]
                    if  hammingDist(leadercode,code) <3:
                          comps[leader].add(v)
                          avail_verts[v] = False
    return comps

def hammingDist(c1,c2):
    dist = bin(c1^c2)
    return dist.count('1')

def hashClustering(g):
    leaders = {v:v for v in g}  # initializing every elem as the single group
    sz = {v:1 for v in g}   #elems number in the group
    for hammcode in hammingcode:
        for vert in g:
            neighbor = hammcode^vert
            if b_nodes[neighbor]:
                quickUnion(vert,neighbor,leaders,sz)
    leaders = {getLeader(v,leaders) for v in leaders}
    return leaders

def quickUnion(vert,neighbor,leaders,sz):
    vl = getLeader(vert,leaders)
    nl = getLeader(neighbor,leaders)
    if sz[vl]>sz[nl]:
        leaders[nl] = vl
        sz[vl] += sz[nl]
    else:
        leaders[vl] = nl
        sz[nl] += sz[vl]

def getLeader(v,leaders):  #get the leader of elem v
    while v != leaders[v]:
        leaders[v] = leaders[leaders[v]]    # path comprression
        v = leaders[v]
    return v

def hammingBase(bit_num,distance):
    baseCode = ('0')*bit_num
    codeset = {baseCode}
    for l in range(1,distance):
        tmpset = set()
        for code in codeset:
            for i in range(bit_num):
                c = list(code)
                c[i] = '1'
                tmpset.add("".join(c))
        codeset|=tmpset
    codeset.discard(baseCode)
    return {int(code,2)  for code in codeset}

def inputData(filename,line_num=None):
    input_data_file = open(filename, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()

    lines = input_data.split('\n')

    first_line = lines[0].split()
    verts_count = int(first_line[0])
    bit_num = int(first_line[1])
    
    b_nodes = bitarray('0'*2**bit_num)
    graph = []
    vert = 0
    for line in lines[1:line_num]:
        if  line.isspace() or len(line)==0:
            continue
        hammingStr = line.split()
        hamming = int("".join(hammingStr),2)
        graph.append(hamming)
        b_nodes[hamming] =True
        vert+=1
    return verts_count,bit_num, graph,b_nodes
   
def getFileName():
    prompt = True
    while prompt:
        filename  = raw_input("Please input data file name: ")
        print "The input data file name is: %r " % filename
        p = raw_input("Does it correct (y/n)?")
        if p=='y':
            prompt = False
    
    if testing:
        folder = './data/'
    else:
        folder = './data/'
    return folder+filename + '.txt'    
    
if __name__ == "__main__":
    
    spacing = 3
    lines = 80000
    filename = getFileName()   
    
    s_time = time.time()
    
    if testing:
        vert_count,bit_num, graph,b_nodes  = inputData(filename,lines+1)
    else:
        vert_count,bit_num, graph,b_nodes  = inputData(filename)
    
    hammingcode = hammingBase(bit_num,spacing)
    g_time = time.time()
    comps = hashClustering(graph)
    print "The clustering number of input graph is: ", len(comps)
    cl_time = time.time()
    
#    naiveMst = naivePrimMst(graph,vertices)
#    naiveCost = np.sum([edges[e]  for e in naiveMst])
#    print "The total cost of the Naive MST is: ", naiveCost
    naive_time = time.time()

    print "Graph creating time:  %s seconds ---" % (g_time - s_time)
    print "Heap clustering running time:  %s seconds ---" % (cl_time - g_time)
    print "Naive Prim running time:  %s seconds ---" % (naive_time - cl_time)
    print "Total running time:  %s seconds ---" % (time.time() - s_time)

