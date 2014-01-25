# -*- coding: utf-8 -*-
"""
Created on Mon Dec 09 17:58:34 2013

@author: gruenewa
"""
from itertools import *

permutand = "123456789"
permutand = "123456789"
const = 2

"""um doppelte zu verhindern, müsste man einfach ein set von permutationen erzeugen (?)"""
multi1min = 1
multi1max = 4
multi2min = 1
multi2max = 4


def solveproblem():
    listofpermutations = permutations(permutand)
    #print [x for x in listofpermutations]
    setofpermutations = set()

    
    for oneitem in listofpermutations:
        #print oneitem
        for m1 in range(multi1min,multi1max+1,1):
            for m2 in range(multi2min,multi2max+1,1):
                multi1 = int(''.join(oneitem[:m1]))
                multi2 = int(''.join(oneitem[m1:m1+m2]))
                product = int(''.join(oneitem[m1+m2:]))
                if multi1*multi2 == product:
                    print multi1, multi2, product
                    setofpermutations.add(product)
    
    print sum(list(setofpermutations))
    
solveproblem()    