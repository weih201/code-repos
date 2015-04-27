# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 03:30:44 2015

@author: hwei
"""
import time
import myHeap as hp

ModSize = 10000 
Testing = False
  
def mediansSum(numlist):
    medians = []
    
    Hlow = hp.maxHeap()
    Hhi = hp.minHeap()
    for num in numlist:
        Hlow.insert(num)
        
        adjustHeaps(Hlow,Hhi)
        medians.append(Hlow.peepRoot())
    return sum(medians)%ModSize

def adjustHeaps(Hlow,Hhi):
    htmp = None
    ltmp = Hlow.peepRoot()
    if not Hhi.isEmpty():
        htmp = Hhi.peepRoot()
        if ltmp>htmp:
            ltmp = Hlow.getRoot()
            htmp = Hhi.getRoot()
            Hhi.insert(ltmp)
            Hlow.insert(htmp)
        
    if Hlow.size() > (Hhi.size()+1):
        tmp = Hlow.getRoot()
        Hhi.insert(tmp)
    
if __name__ == "__main__":
    s_time = time.time()
     
    if Testing:
        f = open("./test/q2e82.txt", "r")
    else:
        f = open("./data/Median.txt", "r")
    numstrlist = list(f)
    numlist = [int(intstr) for intstr in numstrlist]
    
    print mediansSum(numlist)
    
