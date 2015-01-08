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
# I am using a stackoverflow function to generate prime numbers
# I do this, because my sieve is not as optimized as any other prime generating lib
import numpy as np

## this set is unused
#pandigital_set = set(['1','2','3','4','5','6','7','8','9'])
#
#
#def check_for_pandigitalism(number, nozero = False):
#    # this function also matches for a zero (e.g. 102). Do additional check if you want to exclude zero
#    # convert number to string
#    # add each character to a set
#    # if character already present, it is not a pandigital number
#    
#    result = True
#    
#    str_number = str(number)
#    set_number = set()
#    
#    if nozero == True:
#        # adding a 0 to the set will break the function, if a "0" is found in the number to test
#        set_number.add("0")
#    
#    for character in str_number:
#        if character not in set_number:
#            set_number.add(character)
#        else:
#            # print "duplicate found, not a pandigital number"
#            result = False    
#            break
#   
#    return result


# faster function (2x) than the one above
def check_for_pandigitalism(number, nozero = False, nonine = False, noeigth = False):
    counter = 10*[0]
    result = True    
    
    # adding a 0 to the counter will falsify the result, if a "0" is found in the number to test
    if nozero == True:
        counter[0] = 1
       
    if nonine == True:
        counter[9] = 1
        
    if noeigth == True:
        counter[8] = 1        
    
    while number > 0:    
    
        first_digit = number % 10
        if counter[first_digit] == 0:
            counter[first_digit] = 1
        else: 
            result = False
            break
            
        number = number // 10    

    return result

    
def primesfrom2to(n):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = np.ones(n/3 + (n%6==2), dtype=np.bool)
    sieve[0] = False
    for i in xrange(int(n**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[      ((k*k)/3)      ::2*k] = False
            sieve[(k*k+4*k-2*k*(i&1))/3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0]+1)|1)]        
    

def solve_problem():  
    # create a list of primes < 987654321 (largest pandigital number)
    # check from largest to smallest prime for pandigitalism
    upper_bondary = 7654321 + 1
    # lower_bondary = 987624321
    list_of_primes = []
    # generating 50 million primes takes about 10 seconds
    list_of_primes = primesfrom2to(upper_bondary)
    #print list_of_primes
    print str(len(list_of_primes)) + " primes have been generated."
    print "searching for pandigitalism..."
    for prime in reversed(list_of_primes):
        if check_for_pandigitalism(prime, True, True, True):
            print "Largest pandigital prime is:"
            print prime
            break
    
    return 0
    
    
profile.run('solve_problem()')   

"""
output for upper_bondary = 987654321 + 1:
for a 9 digit number, there is no pandigital prime, since:

50251452 primes have been generated.
searching for pandigitalism...
Largest pandigital prime is:
98765431
         44556998 function calls in 624.837 seconds
         
this leaves out the 2  

so, there is another search with an 8 digit number
upper_bondary = 87654321 + 1       
"""         

"""
no 8 digit either

5088942 primes have been generated.
searching for pandigitalism...
Largest pandigital prime is:
8765423
         4501150 function calls in 50.269 seconds
         
"""
"""

518012 primes have been generated.
searching for pandigitalism...
Largest pandigital prime is:
7652413
         175 function calls in 0.049 seconds  
         
is the correct answer         
"""