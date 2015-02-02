import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line


def mapper(record):
    # key: Matrix id
    # value: matrix elem
    val=record[3]
    if record[0]=="a":
       for k in range(5):
           mr.emit_intermediate((record[1],k), (record[2],val))
    elif record[0]=="b":
       for i in range(5):
           mr.emit_intermediate((i,record[2]), (record[1],val))


def reducer(key, elems):
    # key: (i,j)
    # value: list of matrix elem
    indexes = set(map(lambda x:x[0], elems))
    grplist = [[y[1] for y in elems if y[0]== j] for j in indexes]
    grplist = [y for y in grplist if len(y)==2]
    val = sum([y[0]*y[1] for y in grplist])
        
    mr.emit((key[0],key[1], val))



# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
    
