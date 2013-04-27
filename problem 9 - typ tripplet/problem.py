# -*- coding: utf-8 -*-
"""
Created on Wed Apr 03 23:25:50 2013

@author: ventilator

a^2 + b^2 = c^2


a + b + c = 1000

a < b < c


if a = b = c, 3c=1000 -> a = 333 (max)
"""
thousend = 1000
third    = 333

for a in range(1,third+1):
    for b in range(a,thousend-a):
        c = thousend - a - b      
        if a*a + b*b == c*c:
            print a, b, c, a+b+c, a*b*c