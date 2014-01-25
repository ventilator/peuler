# -*- coding: utf-8 -*-
"""
Created on Sat May 18 20:09:09 2013

@author: ventilator
"""

def getsum(length):
    summe = 0
    #length = #of quadrat
    
    
    currentnumber = 1
    summe += currentnumber
    for x in range(2, length+1, 2):
        #print x
        for i in range(0,4):
            currentnumber += x
            summe += currentnumber
            #print x, summe
    
    return summe        
        
    
print getsum(5)   
print getsum(1001)  