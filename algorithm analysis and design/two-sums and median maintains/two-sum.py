# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015

@author: hwei
"""
import time
import bisect

Testing = False

T1 = -10000
T2 = 10000
Buck_Size = 21067
hash_table = [set() for i in range(Buck_Size)]

def count2sum_hash(numlist,t1,t2,buck_size):
    count = 0
    for t in range(t1,t2+1):
        ct = 0
        for i in numlist:
            if i<t-i:
                if (t-i) in hash_table[(t-i)%buck_size]:
                    ct += 1
            else:
                break
        count += ct
    return count

def count2sumpairs(numlist,t1,t2):
    e_max = numlist[len(numlist)-1]
    count = 0
    for num in numlist:
        wlo = t1-num
        if wlo>e_max:
            continue
        if wlo<num:
            i = bisect.bisect_right(numlist,num)
            if i<len(numlist):
                wlo = numlist[i]
            else:
                break
            
        whi = t2-num
        if whi >e_max:
            whi = e_max
        if whi < num:
            break
        lo = bisect.bisect_left(numlist,wlo)
        hi = bisect.bisect_right(numlist,whi)
        count += (hi - lo)
    return count
  
if __name__ == "__main__":
    s_time = time.time()
     
    if Testing:
        f = open("./test/q1e6.txt", "r")
    else:
        f = open("./data/algo1_programming_prob_2sum.txt", "r")
    numstrlist = list(f)
    
    l_time = time.time()
    print "Input file string length", len(numstrlist)
    numset = {long(intstr) for intstr in numstrlist}
    numlist = list(numset)
    sortedlist = sorted(numlist)
    
    print "Sorted list length", len(sortedlist)
    sort_time = time.time()
    
#    for num in  sortedlist:
#        slot = num%Buck_Size
#        hash_table[slot].add(num)
#    hash_time = time.time()
    
    count = count2sumpairs(sortedlist,T1,T2)
#    count = count2sum_hash(sortedlist,T1,T2,Buck_Size)
    
    print "The number of 2 sum in [-10000,10000] is : ",count
    print "File loading time:", (l_time - s_time)
    print "Sorting time: ", (sort_time - l_time)
    print "Hashing table creating time: ", (hash_time-sort_time)
    print "Finding tuples time: ", (time.time()-hash_time)
    print "Total time: ", (time.time()-s_time)