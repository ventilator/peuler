# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 22:00:37 2014

@author: ventilator
"""
'''
Since only 3 5 and 7 are prime, only truncable primes can be obeserved which

begin and end with 3 5 and 7
do not contain a 0,2,4,5,6,8 since the truncated version would end with theese

exception: 23


'''

import venti_util
import profile


def give_truncated_number(number):
    
    str_number = str(number)
    output = set()
    
    truncated_number = ''
    for char in str_number:
        truncated_number += char
        #print truncated_number
        output.add(int(truncated_number))
        
    for left in range(1,len(str_number)):
        #print str_number[left:]
        output.add(int(str_number[left:]))
        
    return output    
        
    



def solve_problem():
    
    primes = venti_util.generate_primes(1000000)
    #print primes
    
    solution = 0    
    count = 0
    
    for prime in primes:
        truncated_primes = give_truncated_number(prime)
        
        if truncated_primes.issubset(primes):
            #print prime
            solution += prime
            count += 1
            print str(prime) + ' is the #' + str(count-4) + ' truncable prime. total sum: ' + str(solution-17) 
    
    
    #print give_truncated_number(3797)
    
    
    return 0
    
    
profile.run('solve_problem()')    
    