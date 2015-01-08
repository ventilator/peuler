# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 17:04:48 2015

@author: ventilator
"""
# find the fastest check for pandigitalism


import profile
# I am using a stackoverflow function to generate prime numbers
# I do this, because my sieve is not as optimized as any other prime generating lib
import numpy as np

# this set is unused
pandigital_set = set(['1','2','3','4','5','6','7','8','9'])


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
##    if nozero == True:
##        # adding a 0 to the set will break the function, if a "0" is found in the number to test
##        set_number.add("0")
#    
#    for character in str_number:
#        set_number.add(character)
#        
#    result = (set_number == pandigital_set)
#   
#    return result

def check_for_pandigitalism(number, nozero = False):
    counter = 10*[0]
    result = True    
    
    # adding a 0 to the counter will falsify the result, if a "0" is found in the number to test
    if nozero == True:
        counter[0] = 1
    
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
    upper_bondary = 1000000 # creates 7157 pandigital numbers
    # lower_bondary = 987624321
    list_of_primes = []
    # generating 50 million primes takes about 10 seconds
    list_of_primes = primesfrom2to(upper_bondary)
    #print list_of_primes
    found_pandigital_primes = 0
    print str(len(list_of_primes)) + " primes have been generated."
    print "searching for pandigitalism..."
    for prime in list_of_primes:
        if check_for_pandigitalism(prime, True):
            found_pandigital_primes += 1
            # break
    print "found pandigital primes: " + str(found_pandigital_primes)
    print "check_for_pandigitalism still working?"
    print True == check_for_pandigitalism(987654321)
    return 0
    
    
profile.run('solve_problem()')   