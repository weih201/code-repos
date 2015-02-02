#! /usr/bin/python
#     File        : assign3-stage1.py
#     Author      : wei han (weih 523979)
#     Date  : Fri. Mar. 23, 2012
#     Description:
from Bio import SeqIO
import sys

# get the number of parameters
parameters = sys.argv
argc = len(parameters)

# There is an error if the number of parameters is not equal to 2
if argc != 2:
      print 'Usage assign3-stage1.py filename'
      sys.exit()

# Script name is parameter 0, we want parameter 1
filename = parameters[1] 
access_no = filename.split(".")[0]

# open the file
input_handle = open(filename, "rU")

# parse the file into a list of Seq objects
seqlist = SeqIO.parse(input_handle, "genbank")

rna_list = []  #dictionary list 
number = 1
# print "Found %i records in the file" % len(list(seqlist))

# go through the list of Seq objects
for record in seqlist:
    # get the length of the sequence in the Seq record
    length = len(record.seq);

    for feature in record.features:
        if feature.type=="tRNA":
            tRNAInfo = {}
            tRNAInfo["access_no"] = access_no
            tRNAInfo["tRNA_No"] = "tRNA "+str(number)
            lowIndex = feature.location.start.position
            highIndex = feature.location.end.position
            tRNAInfo["seq"] = str(record.seq[lowIndex:highIndex])
            proStr = str(feature.qualifiers["product"])
            l = len(proStr)
            proStr = proStr[2:(l-2)]
            tRNAInfo["product"] = proStr
            rna_list.append(tRNAInfo)
            number += 1
#end for loop

LEN = len(rna_list)  # the DNA seq number in the file
i=0
while i<LEN:  # loop every DNA item in the list
      # calculating and print DNA sequence item's length
      print ">"+rna_list[i]["access_no"]+", "+rna_list[i]["tRNA_No"]+", "+ rna_list[i]["product"]
      print rna_list[i]["seq"]
      i+=1  # move to next DNA sequnece

# close the opened files    
input_handle.close() 
# end of program
