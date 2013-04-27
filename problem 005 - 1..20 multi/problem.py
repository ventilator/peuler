# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 01:35:15 2013

@author: ventilator
"""

loesung = 11*12*13*14*15*16*17*18*19*20
#print loesung

loesung = 11*3*2*2*13*7*2*15*2*2*2*2*17*3*3*2*19*5*2*2
loesung = 11*3*2*13*7*5*17*19*20*18
loesung = 10*2*19*9*17*7*13*4*11
print loesung

print "check"
divisor = 1
sumreste = 0
while divisor<20:
    divisor += 1
    sumreste += loesung % divisor
    print loesung % divisor
print "rest " + str(sumreste)    
    
    