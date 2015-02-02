import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: id
     mr.emit_intermediate(record[1], record)

def reducer(key, list_of_record):
    # key: id
    # value: list of record
    order=()

    for elem in list_of_record:
      if elem[0]== "order":
        order = elem
        break
        
    for elem in list_of_record:
      if elem[0]== "line_item":
        mr.emit(order+elem)


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
