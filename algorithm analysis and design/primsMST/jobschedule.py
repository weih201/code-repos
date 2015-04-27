# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 00:28:49 2015

@author: hwei
"""

def jobs_schedule(jobs):
    sorted_jobs_ratio = jobs_ranking(jobs)
    sorted_jobs_diff = jobs_ranking(jobs,False)
    
    ration_sum = weight_ct_sum(sorted_jobs_ratio)
    diff_sum = weight_ct_sum(sorted_jobs_diff)
    return ration_sum, diff_sum

def weight_ct_sum(sorted_jobs):
    weighted_ct = []
    ct = 0
    for job in sorted_jobs:
        ct+=job[1]
        weighted_ct.append(ct*job[0])
    return sum(weighted_ct)
    
   
def jobs_ranking(jobs,ratio=True):
    if ratio:
        sorted_jobs=[(job,(float(job[0])/job[1],job[0])) for job in jobs]
    else:
        sorted_jobs=[(job,(job[0]-job[1],job[0])) for job in jobs]
    sorted_jobs.sort(key= lambda x:x[1],reverse=True )
    return [job[0] for job in sorted_jobs]
 
def inputData(filename):
    filename = "./data/"+filename
    input_data_file = open(filename, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()

    lines = input_data.split('\n')

    first_line = lines[0]
    jobs_count = int(first_line)

    jobs = []
    for i in range(1, jobs_count + 1):
        line = lines[i]
        parts = line.split()
        jobs.append((int(parts[0]), int(parts[1])))
    
    return jobs_count,jobs
   
if __name__ == "__main__":
    test1 = [(8, 50),(74, 59),(31, 73),(45, 79),(10, 10),(41, 66)]  ## Ratio: 31814, difference: 31814
    test2 = [(8, 50),(74, 59),(31, 73),(45, 79),(24, 10),(41, 66),
             (93, 43),(88, 4),(28, 30),(41, 13)]  #Ratio: 60213, difference: 61545

    job_count,jobs =  inputData("jobs.txt")
    print "Input jobs count: ",str(len(jobs))

    ratio_sum,diff_sum = jobs_schedule(jobs)   ##scheduling jobs
    print "Weighted completion time sum (ration): ",ratio_sum
    print "Weighted completion time sum (diff): ",diff_sum
    
