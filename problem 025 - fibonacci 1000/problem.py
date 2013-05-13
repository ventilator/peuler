# -*- coding: utf-8 -*-
"""
Created on Fri May 03 23:45:55 2013

@author: ventilator
"""

zahl1 = 1
zahl2 = 1
zahl3 = 2
length = 1000
term = 2

while zahl3 // 10**(length-1) < 1:
    zahl3 = zahl2 + zahl1
    zahl1 = zahl2
    zahl2 = zahl3
    
    term += 1
    #print term, zahl3
    
print term, zahl3