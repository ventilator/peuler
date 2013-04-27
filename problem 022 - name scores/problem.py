# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 17:26:49 2013

@author: ventilator
"""
def alphavalue(name):
    summe = 0
    for i in name:
        summe += ord(i) - 64
    return summe    


filename = 'names.txt'


with open(filename, 'r') as f:
    read_data = f.read()
f.closed

#create a list out of the long string
data = read_data.split(",")

sdata = []
for i in data:
    i = i.strip('"')
    sdata.append(i)

sdata.sort()

#list is now sorted and ready for eval

summe = 0
for i,s in enumerate(sdata):
    summe += (i+1)*alphavalue(s)
    #i = listenplatz -1
    #s = name
    
print summe

 
    
