#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import shuffle,randint
import time

class myQueue: 
    def __init__(self, bufsize=200): 
        self.q = [] 
        self.out = 0 
        self.bufsize = bufsize
    def push(self, seq): 
        self.q.append(seq) 
    def pop(self): 
        if not self.isEmpty():
            k = self.q[self.out] 
            self.out += 1 
            if self.out>self.bufsize:
                self.q = self.q[self.out:]
                self.out = 0
            return k 
        else:
            return
    def isEmpty(self):
         return self.size() == 0   
    def size(self,used=True):
        if used:
            return len(self.q[self.out:])  
        else:
            return len(self.q)  
    def show(self,used =True):
        if used:
            print self.q[self.out:]
        else:
            print self.q

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
#    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    g = edgesToGraph(edges)
    color_count, node_colors = force_contraction(g,2)

    # prepare the solution in the specified output format
    output_data = str(color_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, node_colors))

    return output_data

def force_contraction(g,loops =5):
    nodes = g_degree_sort(g)
    count, node_colors= HC_Coloring(g,nodes,10000)
    
    for loop in range(loops):
        color_list = list(set(map(lambda color:color, node_colors)))    ##retriving used color set
        color_groups = {color:[i for i in range(len(node_colors)) if node_colors[i]==color] for color in color_list}
        color_list.sort(key = lambda x: len(color_groups[x]))   ## sorting ru group via the set size in the color_groups
        l = int(len(color_list)*0.2)
        contracted_colors = color_list[:l]
        reserved_colors = color_list[l:]
        contracted_nodes = []
        for color in contracted_colors:
            contracted_nodes += color_groups[color]
        shuffle(contracted_nodes)
        reserved_color_num = len(reserved_colors)
        append_size = len(contracted_nodes)/reserved_color_num 
        append_size = append_size if  len(contracted_nodes)%reserved_color_num ==0 else append_size+1
        i=0
        for color in reserved_colors:
            color_groups[color]+=contracted_nodes[i*append_size:(i+1)*append_size]
            i+=1
        nodes = [node for color in reserved_colors for node in color_groups[color]]
        count, node_colors= HC_Coloring(g,nodes,10000)
    return count, node_colors
                
def hillClimbingColoring(g,loops =10000):
    nodes = g_degree_sort(g)
    count, node_colors= HC_Coloring(g,nodes,loops)
    return count, node_colors

def HC_Coloring(g,nodes,loops=10000):
    count, node_colors = wp_coloring(g,nodes)
    
    for loop in range(loops):
        pai_group,ru_group,color_groups = partitionColorGrp(node_colors)
        
        color_groups = perturbation(g,pai_group,ru_group,color_groups)
        color_list = pai_group+ru_group
        shuffle(color_list)
        nodes = [node for color in color_list for node in color_groups[color]]
        count, node_colors = wp_coloring(g,nodes)
    return count, node_colors
    

def perturbation(g,pai_group,ru_group,color_groups):
    ru_set_vert = [(color,vert) for color in ru_group for vert in color_groups[color]]
    for ru_color,vert in ru_set_vert:
        p_min = randint(1,15)
        if p_min>14:      # 30% ratio select elem from the smallest size color set
            for pai_color in pai_group:
                if is_feasiable(g,color_groups[pai_color],vert):
                    color_groups[pai_color].append(vert)
                    color_groups[ru_color].remove(vert)
                    break
    return color_groups

def is_feasiable(g,group,node):
    for vert in g[node]:
        if vert in group:
            return False
    return True

def partitionColorGrp(node_colors):
    color_list = list({color for color in node_colors})
    shuffle(color_list)
    l = int(len(color_list)*.6)
    pai_grp = color_list[:l]
    ru_grp = color_list[l:]
    color_groups = {color:[i for i in range(len(node_colors)) if node_colors[i]==color] for color in color_list}
    ru_grp.sort(key = lambda x: len(color_groups[x]))   ## sorting ru group via the set size in the color_groups
    return  pai_grp,ru_grp,color_groups
    
def g_degree_sort(g):
    degrees =[(x,len(g[x])) for x in g]
    degrees.sort(key = lambda x:x[1], reverse =True)
    return [vert for (vert,edges) in degrees]


def bestRandomColoring(g,loops=2000):
    color_count = len(g)
    node_colors = []
    
    for i in range(loops):
        nodes = g_degree_sort(g)
        shuffle(nodes)
        c_count,colors = wp_coloring(g,nodes)
        if c_count<color_count:
            color_count = c_count
            node_colors = colors
    return color_count,node_colors

def wp_coloring(g,nodes):
    node_colors = [-1]*len(nodes)
    color = -1

    while len(nodes)>0:    # when the node list is not empty
        color += 1
        color_set = set()  # nodes in this coloring

        for node in nodes:
            b_coloring = True
            for v in g[node]:
                if v in color_set:
                    b_coloring = False
                    break
            if b_coloring:
                node_colors[node] = color  # coloring node with color
                color_set.add(node)    ## adding node to the color set
        tmp = [node for node in nodes if node_colors[node]==-1]
        nodes  = tmp
    return color+1, node_colors

def bfs_coloring(g):    
    color_count = len(g)
    node_colors = []
    
    for node in g:
        c_count,colors = bfs_color(g,node)
        if c_count<color_count:
            color_count = c_count
            node_colors = colors
    return color_count,node_colors

def bfs_color(g,s_node):
    usedColor = set()
    node_colors = [0]*len(g)
    b_colored = [False]*len(g)
    queue = myQueue()
    
#    s_node = g_val_sort(g)[0]
    queue.push(s_node)
    b_colored[s_node] =True
    usedColor.add(0)
    
    while not queue.isEmpty():
        v = queue.pop()
        for node in g[v]:
            if not b_colored[node]:
                neighbor_color = set()
                for vert in  g[node]:
                    if b_colored[vert]:
                        neighbor_color.add(node_colors[vert])
                possible_color = usedColor - neighbor_color
                
                if  possible_color == set():
                    node_color = max(usedColor)+1
                    usedColor.add(node_color)
                    node_colors[node] = node_color
                else:
                    node_colors[node] = list(possible_color)[0]
                queue.push(node)
                b_colored[node] =True
    return len(usedColor),node_colors       


def edgesToGraph(edges):
    graph = {}
    for (v1,v2) in edges:
        if graph.has_key(v1):
            graph[v1].append(v2)
        else:
            graph[v1] = [v2]

        if graph.has_key(v2):
            graph[v2].append(v1)
        else:
            graph[v2] = [v1]
    return graph


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        
        start_time = time.time()
        print solve_it(input_data)
        print "Total running time (s): ", time.time()-start_time
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

