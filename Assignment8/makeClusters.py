#!/usr/local/bin/python

# all code here stolen shamelessly from 
# "Programming Collective Intelligence, Chapter 3"

import sys

sys.path.insert(0, '../libs')

import clusters

blognames,words,data=clusters.readfile('blogDataClean.txt')

print "For k=5"
kclust=clusters.kcluster(data, k=5)
print

print "For k=10"
kclust=clusters.kcluster(data, k=10)
print

print "For k=20"
kclust=clusters.kcluster(data, k=20)
print