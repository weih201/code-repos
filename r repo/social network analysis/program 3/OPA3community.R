# Coursera SNA optional Programming Assignment 3 template

# see this blog post for a nice overview of community detection algorithms
# http://www.r-bloggers.com/summary-of-community-detection-algorithms-in-igraph-0-6/

# load the igraph library
# you may have to install this module if you haven't already
library(igraph)

# read in the graph in GML format
# it is a sampled collection of pages from a strange set of seed categories:
# Math, Sociology, and Chemistry
# Change this to be your local file location
#  if you are using Windows, replace the \ in the path with a double \, e.g.
# g = read.graph("C:\\Users\\rool\\Documents\\My Dropbox\\Education\\Social Network Analysis\\Week 3\\wikipedia.gml",format="gml")

g = read.graph("C:/my home/coursera/Other ML and Data Science courses/Social Network Analysis/Home works/programming/program 3/wikipedia.gml",format="gml")

# obtain summary information about the graph
summary(g)

# find the maximal k-core any vertex belongs to
max(graph.coreness(as.undirected(g)))

# find the largest clique using cliques(), also making sure the graph is treated as undirected
length(largest.cliques(as.undirected(g))[[1]])


# fastgreedy community finding algorithm
fc = fastgreedy.community(as.undirected(g))

# community sizes
fcs<-sizes(fc)
fcs <- sort(fcs,decreasing=TRUE)

##  calculating the four largest communities comprise roughly what percentage of the graph
sum(fcs[1:4])/sum(fcs)

# membership in 30th community
V(g)$label[membership(fc)==30]

# InfoMap community finding algorithm (can be slow)
imc = infomap.community(g)
imcs<-sizes(imc)
imcs<- sort(imcs,decreasing=TRUE)

# find the nodes in the largest clique
V(g)$label[largest.cliques(as.undirected(g))[[1]]]

# use modularity() to find the modularity of any given partition
modularity(fc)
modularity(imc)
