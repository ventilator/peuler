# -*- coding: utf-8 -*-
"""
Created on Sun May 19 13:42:40 2013

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
    
power = 5    
powerlist = []   
for i in range(0,10):
    powerlist.append(i**5)
    
print powerlist    
#[0, 1, 32, 243, 1024, 3125, 7776, 16807, 32768, 59049]
'''
eine Zahl mit einer 9 ist mind. 5 stellig.
99999 -> 295245 (6stellig)
999999 -> 354294
Die maximale Summe einer 6stelligen Zahl ist nicht größer als 354294. 
354294 ist also die Obergrenze
'''        
numberslist = []
#maxnumber = 354294
maxnumber = powerlist[9]*6
#start with 2 as 1 is not a sum
for i in range(2,maxnumber+1):
    sumofdigits = 0
    strnum = str(i)
    for s in strnum:
        digit = int(s)
        sumofdigits += powerlist[digit]
    if i == sumofdigits:
        numberslist.append(i)
        print i
        
print 'sum', sum(numberslist)
printtime('sum')        
        
        
        