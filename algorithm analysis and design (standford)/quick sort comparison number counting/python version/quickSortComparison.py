# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:53:03 2015

@author: hwei
"""
import numpy as np

def quicksortcomp(arr, pv):
    count = 0
    if len(arr) <=1:
        return count
    else:
        p = choosePivot(arr,pv)
        less,greater= partition(arr,p)
        count = count + len(arr) - 1
        c_less = quicksortcomp(less,pv)
        c_greater = quicksortcomp(greater,pv)
        return count+c_less + c_greater
                
def partition(arr,l):
    p = arr[l]
    swap(arr,0,l)
    i = 1
#    j = len(arr) - 1
#    while (i <= j):
#        while (arr[i] < p):
#            i += 1
#        while (arr[j] > p):
#            j -= 1
#        if (i <= j):
#            swap(arr,i, j)
#            i += 1
#            j -= 1
#    if j>0 and j<(len(arr)-1):
#       return arr[:j],arr[i:]
#    elif j>0:
#        return arr[:(j+1)],[]
#    else:
#        return [],arr[i:]
    
    for j in range(1,len(arr)):
        if arr[j] < p:
            swap(arr,i,j)
            i = i+1
    swap(arr,0,i-1)
    return arr[:(i-1)],arr[i:]
        
def swap(arr,i,j):
    elem = arr[i]
    arr[i] = arr[j]
    arr[j] = elem
  
def choosePivot(arr,pv):
    if pv == 'f':
        return arr[0]
    elif pv =='l':
        return arr[len(arr)-1]
    else:
        middle =arr[(len(arr)-1)/2]
        med = sorted([arr[0],middle,arr[len(arr)-1]])[1]
#        return med
        if med == middle:
            return (len(arr)-1)/2
        elif med == arr[0]:
            return 0
        else:
            return len(arr)-1
    
if __name__ == "__main__":
    #YOUR CODE HERE
    pv='m'
    with open("./test/1000.txt", "r") as nums:
        array = []
        for num in nums:
            array.append(np.int(num)) 

    print "The length of array: "+str(len(array))
    print  quicksortcomp(array,pv)   

    with open("./data/QuickSort.txt", "r") as nums:
        array = []
        for num in nums:
            array.append(np.int(num)) 

    print "The length of array: "+str(len(array))
    print  quicksortcomp(array,pv)   

