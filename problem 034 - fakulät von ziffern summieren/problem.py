# -*- coding: utf-8 -*-
"""
Created on Fri Jan 03 16:59:34 2014

@author: gruenewa
"""
import math
#import matplotlib libary
import matplotlib.pyplot as plot

def splitnumberindigits(number):
    divisor = 1
    digits = []

    while number / divisor > 0:
        divisor = divisor * 10
        rest = (number % divisor) / (divisor / 10)
        digits.append(rest)
        number = number - rest
    #print digits
        
    
    return digits

def solveproblem():
    number = 1
    x = []
    y = []
    
    while number < 2000000:
    
    
        #number = 145
        digits = splitnumberindigits(number)
        #print number, digits
        factorialdigits = map(math.factorial,digits)
        sumoffactorialdigits = sum(factorialdigits)
        #print number, sumoffactorialdigits
        x.append(number)
        y.append(sumoffactorialdigits)
        if number == sumoffactorialdigits:
            print number, '.....'
            
        number += 1    
    
    
    #plot data
    plot.clf()
    plot.plot(x, y)
    plot.plot(x, x)
    
    #show plot
    plot.show()
    return 0
    
    
solveproblem()    
#limit is a guess, http://en.wikipedia.org/wiki/Factorion explaines why it worked anyway...
#an optimization would be a list of precalculated n! from 0 to 9