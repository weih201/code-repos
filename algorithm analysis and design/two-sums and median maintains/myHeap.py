# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 17:19:10 2015
@author: hwei
"""
from sys import maxint
minint = -maxint-1

class Heap:
    def __init__(self):
        self.heap = []  
        self.val2index ={}
         
    def isEmpty(self):
        return self.size() == 0   

    def insert(self, vert):
        self.heap.append(vert)  
        index = self.size()-1
        self.val2index[vert] = index
        self.bubbleup(index)
        
    def remove(self,elem):
        i = self.val2index.get(elem,-1)
        if i>-1:
            self.removeAt(i)
    
    def removeAt(self,index):
        if not (index<0 or index>=self.size()):
            tmp = self.heap[index]
            del self.val2index[tmp]
            tail = self.heap.pop()
            if index<self.size():
                self.heap[index] = tail
                self.val2index[tail] =index
                self.pushdown(index)

    def peepRoot(self):
        root = self.heap[0]
        return root 

    def getRoot(self):
        root = self.heap[0]
        tmp  = self.heap.pop()
        if self.size()>0:
            self.heap[0] = tmp
            self.val2index[tmp] = 0
            self.pushdown(0)
        return root 

    def swap(self,i,j):
        elem_i = self.heap[i]
        elem_j = self.heap[j]
        self.heap[i] = elem_j
        self.heap[j] = elem_i
        self.val2index[elem_i] = j
        self.val2index[elem_j] = i
     
    def bubbleup(self,i):
        pass 

    def pushdown(self,i):
        pass 

    def size(self):
        return len(self.heap)  
         
    def show(self):
        print self.heap    

class minHeap(Heap):
    def __init__(self):
        Heap.__init__(self)  
         
    def bubbleup(self,i):
        if i==0:
            return
        parent = (i-1)/2
        smallest = parent
        
        vparent = self.heap[parent]
        velem = self.heap[i]
            
        if (velem < vparent): 
            smallest = i
        if smallest <> parent:
            self.swap(smallest,parent)
            self.bubbleup(parent)

    def pushdown(self,i):
        if i<0:
            return
        minimum = self.heap[i]
        iminimum = i
        parent  = i
        
        left = 2*(i+1)-1
        right = 2*(i+1)
        
        vleft  = maxint
        vright = maxint

        if left < self.size():
            vleft = self.heap[left]
        if right < self.size():
            vright = self.heap[right]
            
        if vleft < minimum:
            minimum = vleft
            iminimum = left
        if vright < minimum:
            minimum = vright
            iminimum = right
        if iminimum <> parent:
            self.swap(parent,iminimum)
            self.pushdown(iminimum)
            
 
class maxHeap(Heap):
    def __init__(self):
        Heap.__init__(self)  
         
    def bubbleup(self,i):
        if i==0:
            return
        parent = (i-1)/2
        largest = parent
        
        vparent = self.heap[parent]
        velem = self.heap[i]
            
        if (velem > vparent): 
            largest = i
        if largest <> parent:
            self.swap(largest,parent)
            self.bubbleup(parent)

    def pushdown(self,i):
        if i<0:
            return
        maximum = self.heap[i]
        imaximum = i
        parent  = i
        
        left = 2*(i+1)-1
        right = 2*(i+1)
        vleft = minint
        vright = minint
        
        if left < self.size():
            vleft = self.heap[left]
        if right < self.size():
            vright = self.heap[right]
            
        if vleft > maximum:
            maximum = vleft
            imaximum = left
        if vright > maximum:
            maximum = vright
            imaximum = right
        if imaximum <> parent:
            self.swap(parent,imaximum)
            self.pushdown(imaximum)

