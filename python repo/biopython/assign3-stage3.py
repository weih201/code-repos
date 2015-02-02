#! /usr/bin/python
#     File        : assign3-stage1.py
#     Author      : wei han (weih 523979)
#     Date  : Fri. Mar. 23, 2012
#     Description:
from Bio import Entrez
from Bio import SeqIO
import os
import sys

# parameters is a list or array which holds the commandline parameters
parameters = sys.argv

# get the number of parameters
argc = len(parameters)

# There is an error if the number of parameters is not equal to 2
if argc != 2:
      print 'Usage assign3-stage3.py access_number'
      sys.exit()

os.environ['http_proxy']=''

# Script name is parameter 0, we want parameter 1
database = 'nuccore'
# get the input access number
access_no = parameters[1].split(".")[0]

# Need your email address when querying Entrez
Entrez.email = 'weih@student.unimelb.edu.au'
localfile = 'localfile'

# Query the Entrez database
try:
      search_handle = Entrez.esearch(db=database,term=access_no, usehistory="y", retmax=1)
      search_results = Entrez.read(search_handle)
      search_handle.close()
except:
        print "\nCancelled: Problem with network connection."
        exit(1)   

# Write number of sequences found
gi_list = search_results["IdList"]
##count = int(search_results["Count"])
##print count,
##print 'Sequence found.'

fetch_handle = Entrez.efetch(db="nucleotide", id=gi_list[0], rettype="gb", retmode="text")

out_handle = open(localfile, "w")
out_handle.write(fetch_handle.read())
out_handle.close()
fetch_handle.close()

# open the file
input_handle = open(localfile, "rU")
# parse the file into a list of Seq objects
seqlist = SeqIO.parse(input_handle, "genbank")

rna_list = []     #tRNA dictionary list 
ref_list = []     #reference dictionary list
number = 1
# print "Found %i records in the file" % len(list(seqlist))

# go through the list of Seq objects
for record in seqlist:
    # get the length of the sequence in the Seq record
    length = len(record.seq);

    Organism = "Organism: "+str(record.annotations["organism"])
      
    for reference in record.annotations["references"]:
            refInfo = {}
            refInfo["Authors"] = str(reference.authors)
            refInfo["Title"] = str(reference.title)
            refInfo["Journal"] = str(reference.journal)
            ref_list.append(refInfo)

    for feature in record.features:
          if feature.type=="tRNA":
                tRNAInfo = {}
                tRNAInfo["access_no"] = access_no
                tRNAInfo["tRNA_No"] = "tRNA "+str(number)

                lowIndex = feature.location.start.position
                highIndex = feature.location.end.position
                                    
                tRNAInfo["lowIndex"] = lowIndex
                tRNAInfo["highIndex"] = highIndex
                                    
                tRNAInfo["seq"] = str(record.seq[lowIndex:highIndex])
                proStr = str(feature.qualifiers["product"])
                l = len(proStr)
                proStr = proStr[2:(l-2)]
                tRNAInfo["product"] = proStr
                tRNAInfo["strand"] = str(feature.strand)
                                    
                rna_list.append(tRNAInfo)
                number += 1
#end for loop

out_handle = open("assign3-stage3.out", "w")

LEN = len(rna_list)  # the DNA seq number in the file
i=0
while i<LEN:  # loop every DNA item in the list
      # calculating and print DNA sequence item's length

      print ">"+rna_list[i]["access_no"]+", "+rna_list[i]["tRNA_No"]+\
            ", "+ rna_list[i]["product"]
      print rna_list[i]["seq"]
        
      if rna_list[i]["strand"] == "1":
            strandStr = "forward"
      else:
            strandStr = "reverse"
      
      saveStr = rna_list[i]["tRNA_No"]+", " + rna_list[i]["product"]+", " \
                + str(rna_list[i]["lowIndex"])\
                +" -> "+str(rna_list[i]["highIndex"])+", "+strandStr+"\n"
      
      out_handle.write(saveStr)          
      i+=1  # move to next DNA sequnece

out_handle.write("\n"+Organism+"\n\n")

for ref in ref_list:
      out_handle.write("\nAuthors: "+ref["Authors"]+"\n")
      out_handle.write("Title: "+ref["Title"]+"\n")
      out_handle.write("Journal: "+ref["Journal"]+"\n")

# close the opened files    
input_handle.close()
out_handle.close()
# end of program
