# -*- coding: utf-8 -*-
"""
Created on Wed May 01 11:59:44 2013

@author: ventilator
"""
import itertools

rank   = 1000000
digits = 10
#rank = 2
#digits = 3

#create arry with digits
number = []
for i in range(digits):
    number.append(i)    
number.reverse
#


permutations = list(itertools.permutations(number))

def printpermutations(rank,permutations):
    #print permutations
    if rank <= len(permutations):
        print rank,permutations[rank-1],int(''.join(str(x) for x in (permutations[rank-1])))
        
        
printpermutations(1,permutations)        
printpermutations(rank,permutations)
printpermutations(len(permutations),permutations)


