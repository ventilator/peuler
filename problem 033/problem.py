# -*- coding: utf-8 -*-
"""
Created on Fri Jan 03 16:59:34 2014

@author: gruenewa
"""
import math

def splitnumberindigits(number):
    divisor = 1
    digits = set()

    while number / divisor > 0:
        divisor = divisor * 10
        rest = (number % divisor) / (divisor / 10)
        digits.add(rest)
        number = number - rest
    #print digits
        
    
    return digits

def solveproblem():
    number = 1
    while number < 1000000:
    
    
        #number = 145
        digits = splitnumberindigits(number)
        factorialdigits = map(math.factorial,digits)
        sumoffactorialdigits = sum(factorialdigits)
        #print number, sumoffactorialdigits
        if number == sumoffactorialdigits:
            print number, '.....'
            
        number += 1    
    
    
    return 0
    
    
solveproblem()    