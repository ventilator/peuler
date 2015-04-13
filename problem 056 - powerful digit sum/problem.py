# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:22:16 2015

@author: gruenewa
"""
import profile

        
def digital_sum(number):
    string = str(number)
    digit_sum = 0
    for s in string:
        digit_sum += int(s)

    return digit_sum



def solve_problem():
    
    a_max = 100
    b_max = 100
    max_digital_sum = 1
    
    for a in range(a_max):
        for b in range(b_max):
            max_digital_sum = max(max_digital_sum, digital_sum(a**b))

            
    print(max_digital_sum)
    
    return 0
    
    
profile.run('solve_problem()')   
