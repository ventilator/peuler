# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014
@author: ventilator 

The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28. In fact, there are exactly four numbers below fifty that can be expressed in such a way:

28 = 22 + 23 + 24
33 = 32 + 23 + 24
49 = 52 + 23 + 24
47 = 22 + 33 + 24

How many numbers below fifty million can be expressed as the sum of a prime square, prime cube, and prime fourth power?
"""

import time
start_time = time.time()        
    
import math

prime_filename = "..\\primes\\primes1.txt"    
prime_filename = "primes7069.txt"    # contains prime numbers up to max_c
max_n = 50 * 10**6
# max_n = 50 # test case

max_c = math.floor(math.pow(max_n, 1/4))
max_b = math.floor(math.pow(max_n, 1/3))
max_a = math.floor(math.pow(max_n, 1/2))    

print("max_c, max_b, max_a")
print(max_c, max_b, max_a)

def load_primes(prime_filename):
    f = open(prime_filename)           
    data = []
    for line in f:
        data.append(str.split(line))
      
    data = list(map(int, data[0]))  # flat list and convert to int    
    return data
    
def test(a,b,c):
    return a + b + c < max_n    
        

def solve_problem():
    primes = load_primes(prime_filename)           
    list_c = list(filter(lambda n: n <= max_c, primes))
    list_c = [n**4 for n in list_c]
    list_b = list(filter(lambda n: n <= max_b, primes))
    list_b = [n**3 for n in list_b]
    list_a = list(filter(lambda n: n <= max_a, primes))
    list_a = [n**2 for n in list_a]

    valid_count = 0
    numbers = set()
    
    for c in list_c:
        for b in list_b:
            for a in list_a:
                summe = a + b + c
                if summe < max_n:
                    if summe not in numbers:
                        numbers.add(summe)
                        valid_count+= 1
                    # print(a + b + c)
    
    print("Number of combinations:")                
    print(valid_count) # 1097343
    return 0
    
    
solve_problem()  
print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))

#import profile 
#profile.run('solve_problem()')   

"""
nice solution from forum:

from Euler import sieve
from itertools import product

print len({a**2+b**3+c**4 for a,b,c in product(sieve(7072),sieve(369),sieve(85)) if a**2+b**3+c**4<50*10**6})
"""