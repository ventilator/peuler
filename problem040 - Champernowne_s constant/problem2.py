# -*- coding: utf-8 -*-
"""
Created on Wed Jan 07 08:49:00 2015

@author: ventilator

this program prints the number 210 to solve problem 40
"""

import profile, math



def give_digit_of_ractional_part(digit_to_find):
    # current integer to append
    counter = 0
    # track of sum of length of all integers: digit
    position = 0
    while position < digit_to_find:
        counter += 1
        counter_str = str(counter)
        position += len(counter_str)
        
    print "counting stopped, was searching for digit :" + str(digit_to_find)
    print "digit at position: "+ str(position) + " is made from"
    print "this number: "+ counter_str    
        
    digits_to_go_back = position - digit_to_find
    print "we go back by: " + str(digits_to_go_back)
    
    print "you are looking for: " + counter_str[-(digits_to_go_back + 1)]    
    
    return int(counter_str[-(digits_to_go_back + 1)])    
    



def solve_problem():
#    give_digit_of_ractional_part(1)
#    give_digit_of_ractional_part(10)
#    give_digit_of_ractional_part(12)
#    give_digit_of_ractional_part(100)    
#    
#    for i in range(1,20):
#        give_digit_of_ractional_part(i)        
    
    max_power_of_10 = 6
    produkt = 1
    exponent = 0 
    while exponent < max_power_of_10:
        digit_to_find = 10**exponent
        produkt *= give_digit_of_ractional_part(digit_to_find)
        print produkt
        exponent += 1
    
    print "solution:"
    print produkt    
    
    return 0
    
    
profile.run('solve_problem()')   