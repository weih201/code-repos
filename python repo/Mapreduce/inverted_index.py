import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    id = record[0]
    text = record[1]
    words = text.split()
    for w in words:
      mr.emit_intermediate(w, id)

def reducer(key, list_of_id):
    # key: word
    # value: list of id
    id_lst=[]
    for v in list_of_id:
      id_lst.append(v)
    mr.emit((key, list(set(id_lst))))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
