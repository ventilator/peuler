# -*- coding: utf-8 -*-
"""
Created on Sat May 18 21:46:42 2013

@author: ventilator
"""

#Timing
import time

timing_start = time.clock()

def printtime(reason):
    global timing_start
    print 'The execution took {time:.3f}s. {reason}'.format(time = (time.clock() - timing_start), reason=reason)
    timing_start = time.clock()
#Timing end.    





numbers = []
#print len(numbers)
for a in range(2,101):
    for b in range(2,101):
        number = a**b
        if number not in numbers:
            numbers.append(number)
            
print len(numbers)            

printtime('list')

#improvement using sets
from sets import Set

numbers = Set()
#print len(numbers)
for a in range(2,101):
    for b in range(2,101):
        number = a**b
        numbers.add(number)
            
print len(numbers)            

printtime('set')