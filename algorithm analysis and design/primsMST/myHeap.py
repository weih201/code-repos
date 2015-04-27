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
        self.val2index[vert[0]] = index
        self.bubbleup(index)
        
    def remove(self,elem):
        i = self.val2index.get(elem,-1)  #get the index of elem
        if i>-1:
            self.removeAt(i)   # if elem exists, remove it with its index
    
    def removeAt(self,index):
        if not (index<0 or index>=self.size()):
            tmp = self.heap[index][0]     # get the elem value
            del self.val2index[tmp]     # delete it from val2index map
            tail = self.heap.pop()      # get the last elem in the heap
            if index<self.size():       #if heap is not empty
                self.heap[index] = tail    #insert the tail elem to heap's index location
                self.val2index[tail[0]] =index  #mark the new elem value as index
                self.pushdown(index)    # firstly, pushdown heap
                                        # now index is theminimum elem in its sub-heap 
                self.bubbleup(index)    # we need bubbleup heap from index 
 
    def peepRoot(self):
        if self.size()>0:
            root = self.heap[0]
            return root 

    def getRoot(self):
        if self.size()>0:
            root = self.heap[0]
            del self.val2index[root[0]]
            tmp  = self.heap.pop()
            if self.size()>0:
                self.heap[0] = tmp
                self.val2index[tmp[0]] = 0
                self.pushdown(0)
            return root 

    def swap(self,i,j):
        elem_i = self.heap[i]
        elem_j = self.heap[j]
        self.heap[i] = elem_j
        self.heap[j] = elem_i
        self.val2index[elem_i[0]] = j
        self.val2index[elem_j[0]] = i
     
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
        
        vparent = self.heap[parent][1]
        velem = self.heap[i][1]
            
        if (velem < vparent): 
            smallest = i
        if smallest <> parent:
            self.swap(smallest,parent)
            self.bubbleup(parent)

    def pushdown(self,i):
        if i<0:
            return
        minimum = self.heap[i][1]
        iminimum = i
        parent  = i
        
        left = 2*(i+1)-1
        right = 2*(i+1)
        
        vleft  = maxint
        vright = maxint

        if left < self.size():
            vleft = self.heap[left][1]
        if right < self.size():
            vright = self.heap[right][1]
            
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
        
        vparent = self.heap[parent][1]
        velem = self.heap[i][1]
            
        if (velem > vparent): 
            largest = i
        if largest <> parent:
            self.swap(largest,parent)
            self.bubbleup(parent)

    def pushdown(self,i):
        if i<0:
            return
        maximum = self.heap[i][1]
        imaximum = i
        parent  = i
        
        left = 2*(i+1)-1
        right = 2*(i+1)
        vleft = minint
        vright = minint
        
        if left < self.size():
            vleft = self.heap[left][1]
        if right < self.size():
            vright = self.heap[right][1]
            
        if vleft > maximum:
            maximum = vleft
            imaximum = left
        if vright > maximum:
            maximum = vright
            imaximum = right
        if imaximum <> parent:
            self.swap(parent,imaximum)
            self.pushdown(imaximum)

