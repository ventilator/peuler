# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:33:06 2015

@author: gruenewa


The first two consecutive numbers to have two distinct prime factors are:

14 = 2 × 7
15 = 3 × 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2² × 7 × 23
645 = 3 × 5 × 43
646 = 2 × 17 × 19.

Find the first four consecutive integers to have four distinct prime factors. What is the first of these numbers?
"""

import collections

def factorize(n):
    found_factors = set()
    if n > 0:
        # special case for n=1
        if n == 1:
            found_factors.add(1)        
        
        # account for all mulitples of 2, since they are all 2**x
        if n % 2 == 0:
            found_factors.add(2)
            n = n // 2
            while n % 2 == 0:
                n = n // 2
        
        # find all odd factors
        current_factor = 3
        max_factor = n**0.5
        while n > 1 and current_factor <= max_factor:
            if n % current_factor == 0:
                n = n // current_factor
                found_factors.add(current_factor)
                while n % current_factor == 0:
                    n = n // current_factor
                max_factor = n**0.5
            current_factor += 2
        
        if n > 1:
            found_factors.add(n)
    return found_factors
    
            
def main():    
    max_number = 10**6
    number_of_distinct_factors = 4
    number_of_consecutive_numbers = number_of_distinct_factors
    
    number_of_prime_factors = collections.deque([], number_of_consecutive_numbers)    
    
    # for convenience log also the prime factors and numbers 
    prime_factors = collections.deque([], number_of_consecutive_numbers)    
    numbers = collections.deque([], number_of_consecutive_numbers) 
    
    for i in range(1,max_number):
        # deque that tracks number of prime factors of the last 4 numbers
        factorization = factorize(i)
        number_of_prime_factors.append(len(factorization))        
        
        # just logging
        prime_factors.append(factorization)
        numbers.append(i)                
        
        if number_of_prime_factors.count(number_of_distinct_factors) == number_of_distinct_factors:
            print(numbers, "have the same number of prime factors", "\n", prime_factors)
            break
        

import cProfile
cProfile.run('main()')        