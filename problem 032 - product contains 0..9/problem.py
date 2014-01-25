# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 22:03:55 2013

@author: ventilator
"""

"""
[refere to problem_2.py for solution]
Problem 32:
Preface:
Determine distirbution of digits on multicand (x), multiplier (y)  and product (z)
Since 97*86 = 8342 < 5-digit number, the product is a 4-digit number (or lower)

This leaves 9!/(9-4)! products which are created by x and y
x has up to 4 digits, leaving 1 digit to y,
or #(x)=3 and #(y)=2
everything else is just a swap of x and y

# of possibilities to order 5 remaining: = 5!
of each order, there are 2 spots to put the *:
????*? or ???*??

lets calculate the possibilites:
"""
from math import *
from itertools import *

n = 9
maxdigitsofproduct = 4

def numberofarrangements(n):
    products = factorial(n)/factorial(n-maxdigitsofproduct)
    arrangements = factorial(n-maxdigitsofproduct)
    print "Products:", products
    print "# of arrangements left", arrangements
    print "in total with 2 *-Positions:", products*arrangements*2
    return 0


permutand = "123456789"
permutand = "123"

def sovleproblem():
    listofpermutations = permutations(permutand)
    print [x for x in listofpermutations]
    return 0
    
#numberofarrangements(9)    
sovleproblem()