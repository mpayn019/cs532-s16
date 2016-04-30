import requests
import json

b=0

mementos1 = open('./testfile3.txt' , 'w+')
mementos2 = open('./testfile5.txt' , 'w+')

#Place your data file here
for line in open('linkList.txt','r'):
    
    a = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/' + line
    res= requests.get(a)
    test = open('./testfile2.txt' , 'w+')
    i = 0
    test.write(res.text)
    for line in open('testfile2.txt','r'):
        if 'rel="memento"' in line:
            i = i + 1
    b = b + 1
    mementos1.write(str(i) + '\n')
    #sorts out bad links for carbon date
    if i > 0:
        mementos2.write(a + '\n')
    #sorts out bad links for carbon date
    print b
    print i
    print a