# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:30:51 2015

@author: gruenewa
"""

def n_square(n):
    current = 1
    while current <= n:
        yield current**2
        current += 1
        
        
        
for i in n_square(20):
    print(i)