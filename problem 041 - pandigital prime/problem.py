# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 12:26:59 2015

@author: ventilator

Pandigital prime
Problem 41
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""

import profile
# I am using sympy to generate prime numbers
# I do this, because my sieve is not as optimized as any other prime generating lib
from sympy import sieve

# this set is unused
pandigital_set = set(['1','2','3','4','5','6','7','8','9'])


def check_for_pandigitalism(number):
    # convert number to string
    # add each character to a set
    # if character already present, it is not a pandigital number
    
    result = True
    
    str_number = str(number)
    set_number = set()
    
    for character in str_number:
        if character not in set_number:
            set_number.add(character)
        else:
            # print "duplicate found, not a pandigital number"
            result = False
    
    return result

    
        
    

def solve_problem():
    # create a list of primes < 987654321 (largest pandigital number)
    # check from largest to smallest prime for pandigitalism
    upper_bondary = 987654321
    lower_bondary = 987624321
    list_of_primes = []
    list_of_primes = [i for i in sieve.primerange(lower_bondary, upper_bondary)]
    # print list_of_primes
    print str(len(list_of_primes)) + " primes have been generated"
    print check_for_pandigitalism(4)
    
    return 0
    
    
profile.run('solve_problem()')   