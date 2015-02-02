# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 00:28:49 2015

@author: hwei
"""
import numpy as np

def sort(arr,count):
    if len(arr)<2:
        return arr,count
    else:
        a_left,c_left = sort(arr[:len(arr)/2],count)
        a_right,c_right = sort(arr[len(arr)/2:],count)
        arr, c_merge = merge(a_left,a_right)
        return arr, c_left+c_right+c_merge-count

def merge(left,right):
    i=0
    j=0  
    count = 0
    arr = []
    while i<len(left) and j<len(right):
        if left[i]<right[j]:
            arr.append(left[i])
            i=i+1
        else:
            arr.append(right[j])
            count=count+len(left)-i  #  left[i]>right[j], thus there are 
                                     #  at least len(left)-i elems bigger than right[j']
            j=j+1
    while i<len(left):
        arr.append(left[i])
        i=i+1
    while j<len(right):
        arr.append(right[j])
        j=j+1
    return arr, count
        
def simpleCount(arr):
    count=0
    i=0
    while i<len(arr):
        j=i+1
        while j<len(arr):
            if(arr[i]>arr[j]):
                count=count+1
            j=j+1
        i=i+1
    return count
    
    
    
if __name__ == "__main__":
    #YOUR CODE HERE
      
    test = [4, 80, 70, 23, 9, 60, 68, 27, 66, 78, 12, 40, 52, 53,
            44, 8, 49, 28, 18, 46, 21, 39, 51, 7, 87, 99, 69, 62, 
            84, 6, 79, 67, 14, 98, 83, 0, 96, 5, 82, 10, 26, 48, 
            3, 2, 15, 92, 11, 55, 63, 97, 43, 45, 81, 42, 95, 20, 
            25, 74, 24, 72, 91, 35, 86, 19, 75, 58, 71, 47, 76, 59, 
            64, 93, 17, 50, 56, 94, 90, 89, 32, 37, 34, 65, 1, 73,
            41, 36, 57, 77, 30, 22, 13, 29, 38, 16, 88, 61, 31, 85, 
            33, 54]      # ans = 2372

    with open("./data/IntegerArray.txt", "r") as nums:
        array = []
        for num in nums:
            array.append(np.int(num)) 

    arr,count = sort(array,0)   ## mergecount last about 2 secs
    print count
#    print simpleCount(array)   ## simplecount last about 20 mins