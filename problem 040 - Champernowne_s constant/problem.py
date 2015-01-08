# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator

champernowne = cn
"""

import profile, math

maxorder = 6

def give_digit_of_ractional_part(position):
    #table of space a number needs
    space = []
    
    for n in range(0, maxorder):
        space.append(9*(10**n)*(n+1))        
    
    print space
    
    #calculate power of 10 of position
    order = int(math.floor(math.log10(position)))
    print order
    
    count = 0
    for i,n in enumerate(space):
        if count+n < position:
            count += n
            print position, count
        else:
            count += (position - count) * (i+1)
            print position, count
            break
        
    
    
    



def solve_problem():
    give_digit_of_ractional_part(1)
    give_digit_of_ractional_part(10)
    give_digit_of_ractional_part(100)    
    
    return 0
    
    
profile.run('solve_problem()')   