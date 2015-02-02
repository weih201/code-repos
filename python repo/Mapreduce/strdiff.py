import sys

str1=raw_input("Input the first string")
str2=raw_input("Input the second string")

length = len(str1)

for i in range(length):
    if not str1[i]==str2[i]:
        print "Index at: %d" % i
        print "The remain str in the first str are %s \n" % str1[i:]
        print "The remain str in the second str are %s \n" % str2[i:]
        break
