import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

"""
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, 1)
"""

def reducer(key, list_of_values):
    # key: (i,j)
    # value: list of matrix elem
    for elems in list_of_values:
        indexes = set(map(lambda x:x[0], list))
        grplist = [[y[1] for y in elems if y[0]== j] for j in indexes]
        grplist = [y for y in grplist if len(y)==2]
        val = sum([y[0]*y[1] for y in grplist])
        
    mr.emit((key[0],key[1], val))


# =============================
def prescan(inputdata):
    max_index = {"a": [-1, -1], "b": [-1, -1]}

    for elem in inputdata:
        if elem[0]=="a":
            if elem[1]>max_index["a"][0]:
                max_index["a"][0]=elem[1]
            if elem[2]>max_index["a"][1]:
                max_index["a"][1]=elem[2]
        
        if elem[0]=="b":
            if elem[1]>max_index["b"][0]:
                max_index["b"][0]=elem[1]
            if elem[2]>max_index["b"][1]:
                max_index["b"][1]=elem[2]
    return max_index

def bind_mapper(max_index):
    L = max_index["a"][0] + 1
    M = max_index["a"][1] + 1
    N = max_index["b"][1] + 1

    def mapper(record):
        # The mapper function uses the values of L, M and N
        # defined in the outer call to bind_mapper
        val=record[3]
        if record[0]=="a":
            for k in range(N):
              mr.emit_intermediate((record[1],k), (record[2],val))
        elif record[0]=="b":
            for i in range(L):
              mr.emit_intermediate((i,record[2]), (record[1],val))
            
    return mapper

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    max_index = prescan(inputdata)
    mr.execute(inputdata, bind_mapper(max_index), reducer)


    
