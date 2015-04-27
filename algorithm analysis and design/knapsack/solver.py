#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from copy import deepcopy
import numpy as np
Item = namedtuple("Item", ['index', 'value', 'weight'])

df=False

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
#    step = 1
    
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
        
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    taken = [0]*len(items)
    
    if df:   ## dynamic programming approach
        v_table = dict()
        dp_fill_tbl(capacity, items, v_table)
        
        key = (capacity,(len(items)-1)%2)
        result = v_table.get(key,(0,[]))
        
        value = result[0]
        paths = result[1]
        for i in paths:
            taken[i] = 1
    else:   ## Branch-bound approach
        solution = bb_search(capacity,items)
        value = solution[0]
        for i in solution[1]:
            taken[i] = 1
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def bb_search(room,items):
    items.sort(key=lambda x: (float(x.value)/x.weight,x.value), reverse=True)
    densities = [float(x.value)/x.weight  for x in items]
    
    solution = (0,[])
    if is_almost_equal(densities):
        solution = greedy_search(room,items)
    else:
        solution = bb_dfs(room,items)
    return solution

def bb_dfs(room,items):
    solution = (0,[])
    e_stack = []
    node = (0,room,0,[])
    e_stack.append(node)
            
    while len(e_stack) > 0:
        (val,cap,index,path) = e_stack.pop()
        est = val + getEstimation(cap,items[index:])
        if est<solution[0]:
            continue
            
        if index<len(items)-1:
            e_stack.append((val,cap,index+1,path))
                    
        if index<len(items):
            wt = items[index].weight
            if wt<=cap:
                 p = deepcopy(path)
                 p.append(items[index].index)
                 vl = val+items[index].value
                 e_stack.append((vl,cap-wt,index+1,p))
                 if vl>solution[0]:
                     solution = (vl,p)
    return solution
    
def greedy_search(room,items):
    val = 0
    path = []
    for item in items:
        w = item.weight
        if w<room:
            room -= w
            val += item.value
            path.append(item.index)
    return (val,path)

def is_almost_equal(d):
    d0 =[d[0]]*len(d)
    return sum(np.isclose(d0,d))==len(d)

def getEstimation(room,items):
    optimal = 0
    for item in items:
        w = item.weight
        if w<room:
            room -= w
            optimal += item.value
        else:
            ratio = float(room)/float(w)
            optimal += item.value*ratio
            break
    return optimal

def dp_fill_tbl(capacity,items,v_table):
    for i in np.arange(len(items)):
        for cap in np.arange(capacity+1):
            above = (0,[])
            left = (0,[])
            
            key = (cap,i%2)
            vabove = 0
            pabove = []
            weight = items[i].weight
            
            if cap >= weight:
                kabove = ((cap - weight),(i-1)%2)
                above =  deepcopy(v_table.get(kabove,(0,[])))
                
                vabove = above[0] + items[i].value
                pabove = above[1]
                pabove.append(items[i].index)
               
            if i>0:
                kleft = (cap,(i-1)%2)
                left =  deepcopy(v_table.get(kleft,(0,[])))

            if left[0] > vabove:
                v_table[key] = left
            else:
                v_table[key] = (vabove, pabove)

import sys
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

