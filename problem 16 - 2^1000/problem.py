# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:19:46 2013

@author: Der_Ventilator
"""

num =  2**1000
strnum = str(num)
print strnum

summe = 0
for i in strnum:
    summe += int(i)
    
print summe    