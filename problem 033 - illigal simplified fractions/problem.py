# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 22:49:17 2013

@author: ventilator
"""

"""
problem 33


nontrivial example means, that 1st digit of numerator equals 2nd digit of ,
or vice versa:

case A:

xy/yz = x/z

case B: 
was not programmed, because A already yielded 4 products

"""
def solveproblem():
    endproduct = 1    
    
    
    #y is from 1..9
    for z in range (1,10,1):
        #x is 1..y, because its smaler than y because fraction is <1
        for x in range(1,z,1):
            for y in range (1,10,1):
                numerator = float(x*10 + y)
                denominator = float(y*10 + z)
                fraction = numerator/denominator
                simplified_fraction = float(x)/float(z)
                #this is bad, because it could stumbler across rounding differences
                if simplified_fraction == fraction:
                    print numerator, " / ", denominator, " = ", fraction, " = ", x, " / ", z 
                    endproduct = endproduct*float(x)/float(z)
    
    print endproduct
    #turns out, that 0.01 is 1/100, using brain calculation
    return 0

solveproblem()