# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator


#1: dumb generation of primes would use >1GB memory (MemoryError)
    and 6 digits takes more time than you want to wait (6 seconds)
"""




import venti_util

import profile

max_prime = 987654       
    



def solve_problem():
    
    listofprimes = venti_util.generate_primes(max_prime)
    
    
    return 0
    
    
profile.run('solve_problem()')   