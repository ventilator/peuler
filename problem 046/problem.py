# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 12:48:06 2015

@author: gruenewa
"""
import math


# http://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Prime_number_generation#Python
def prime_sieve(n):
    """Generate the primes less than ``n`` using the Sieve of Eratosthenes."""
    a = [True] * n
    a[0] = a[1] = False
    for i, isprime in enumerate(a):
        if isprime:
            yield i
            for j in range(i * i, n, i):
                a[j] = False


def n_square(n):
    current = 1
    while current <= n:
        yield current**2
        current += 1


# Goldbach's other conjecture
def goc(odd, prime, square):
    return odd == prime + 2*square


def main():
    lut_squares = []
    lut_primes = []
    max_odd_number = 9999
   
    for x in prime_sieve(max_odd_number):
        lut_primes.append(x)
        
    max_square = math.ceil((max_odd_number / 2)**0.5) # n² cannot be higher
    for y in n_square(max_square):
        lut_squares.append(y)

    # print(lut_primes)
    # print(lut_squares)
    
    current_odd = 9
    while current_odd < max_odd_number:
        if current_odd not in lut_primes:
            goc_confirmed = False
            for square in lut_squares:
                current_prime_n = 0
                current_prime = lut_primes[current_prime_n]
                # print("current square " + str(square))
                while current_prime <= current_odd:
                    if not goc(current_odd, current_prime, square):
                        current_prime_n += 1
                        current_prime = lut_primes[current_prime_n]
                    else:
                        # print("goc confirmed")
                        # print(current_odd, current_prime, square * 2)
                        goc_confirmed = True                
                        break
                if goc_confirmed:
                    break
            if goc_confirmed == False:
                print("goc could not be confirmed")
                print(current_odd)        
                break
        current_odd += 2
    
main()    

# by testing up to 9999: 5777 is found as the first number nt withstanding goc testing.

