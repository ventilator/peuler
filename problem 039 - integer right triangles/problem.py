# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator

this solution gives p = 840 with n=8 after 20 seconds (which are less than 1 minute)
"""


import profile

#perimeter = 120
maxp = 1000

        
def checkifrectengulartriangle(a, b, c):
    return a**2 + b**2 == c**2    

def checkifmorethanrectengulartriangle(a, b, c):
    return a**2 + b**2 > c**2        


def solveforperimeter(p,print_rectangle):
    if print_rectangle: print repr("p").rjust(4), repr("n").rjust(5), repr("a").rjust(5), repr("b").rjust(5), repr("c").rjust(5) 
    cmin = p // 3 + p % 3 #since it is the longest side
    cmax = p // 2 #since it cannot be longer than a and b together
    n = 0 #number of solutions
    for c in range(cmin, cmax+1):            
        amin = 1
        amax = (p - c) // 2 #if bigger, b will smaller but already seen as a
        #if p == perimeter: print amin,amax,c
        for a in reversed(range(amin, amax+1)):
            b = p - a - c
            if checkifrectengulartriangle(a, b, c):
                n += 1
                if print_rectangle: print repr(p).rjust(4), repr(n).rjust(5), repr(a).rjust(5), repr(b).rjust(5), repr(c).rjust(5)
                
            # this optimization works because a is reversed, thus only becoming smaller    
            if checkifmorethanrectengulartriangle(a, b, c):                
                break
    return n


def solve_problem():

    pmax = 0
    nmax = 0    
    
    
    # c will be biggest number, a the smallest
    for p in range(3, maxp+1): #3 is the smallest triangle
        n = solveforperimeter(p, False)
        
 
        if n > nmax: 
            pmax = p
            nmax = n
            
    print pmax
    solveforperimeter(pmax, True)        
    
    return 0
    
    
profile.run('solve_problem()')   