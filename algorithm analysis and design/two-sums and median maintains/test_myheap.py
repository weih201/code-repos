# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015

@author: hwei
"""
import myHeap as hp
  
if __name__ == "__main__":
     
#    f = open("./test/q2e148.txt", "r")
    f = open("./data/Median.txt", "r")
    numstrlist = list(f)
    numlist = [int(intstr) for intstr in numstrlist]
    
    Hlow = hp.maxHeap()
    Hhi = hp.minHeap()
    
    print "Hlow is a Heap: ", isinstance(Hlow,hp.Heap)
    
    Hlow.show()
    Hhi.show()
    
    for num in numlist:
        Hlow.insert(num)
        Hhi.insert(num)
    
    Hlow.show()
    Hhi.show()
    
    maxlist = []
    minlist = []
    print "Max heap Hlow:"
    while not Hlow.isEmpty():
        maxlist.append(Hlow.peepRoot())
        print Hlow.getRoot()
    
    print "Min heap Hhi:"
    while not Hhi.isEmpty():
        minlist.append(Hhi.peepRoot())
        print Hhi.getRoot()
    
    Hlow.show()
    Hhi.show()
    
    print "Un-sorted maxlist equals to minlist: ", maxlist==minlist
    print "Sorted maxlist equals to minlist: ", sorted(maxlist)==minlist