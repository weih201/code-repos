import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # record[0]: id
    # record[1]: nucleotides
    l=len(record[1])
    key=record[1][l-10:l]
    nucleotides = record[1][0:l-10]
    mr.emit_intermediate(key, nucleotides)

def reducer(key, nucleotides):
    # key: last ten ch
    # nucleotides: list of values

    for dna in set(nucleotides):
        mr.emit(dna)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
