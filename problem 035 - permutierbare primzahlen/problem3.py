# -*- coding: utf-8 -*-
"""
Created on Wed Jan 08 16:53:44 2014

@author: gruenewa
"""

import math
import itertools
import profile
import venti_util

def generate_primes(max_prime):
    #liste von (ungeraden zahlen), die potentiell prime sind
    #boolean liste, dessen index mit der primzahl verknüpft ist und
    #boolean = true = prime
    #index = number

    primes = [True]*(max_prime+1)
    
    #list, which will contain the primes as numbers
    listofprimes = set() 
    listofprimes.add(2)

    #indices are noted in the form i=prime, so the list start with number 0
    #2,3 are a prime
    #even numbers are ignored by default except number 2, they are never prime
    #sieve starts at 3

    
    #sieve
    index = 3    
    while index < len(primes):
        if primes[index]:            
            listofprimes.add(index) #convert sieve to list of primes
            product = index*index #begin with prime² (optimization)
            while product < len(primes):
                primes[product] = False #set nonprimes to False
                product += index #increase product by one factor                
        index +=2 #ignore even numbers
    #sieve ends      
        
    return listofprimes

def split_number_into_digits(number):
    divisor = 1
    digits = []

    while number / divisor > 0:
        divisor = divisor * 10
        rest = (number % divisor) / (divisor / 10)
        digits.append(rest)
        number = number - rest
    #print digits
        
    
    return digits

def list_of_digits_to_number(digitlist):
    s = ''.join(map(str, digitlist))
    return int(s)

def give_unique_permutations_of_number(number):
    #123 -> [1,2,3]
    permutated_numbers = set()
    for permutated_number in itertools.permutations(str(number)):
        permutated_numbers.add(int(''.join(permutated_number)))
    
    return permutated_numbers


def solveproblem():
    primes = generate_primes(1000000)
    number_of_circular_primes = 0
    
    for prime in primes:
        rotateted_primes = venti_util.give_rotations_of_number(prime)
        if rotateted_primes.issubset(primes):
                number_of_circular_primes += 1           
                print rotateted_primes               

    print 'number_of_circular_primes', number_of_circular_primes
    return 0
    
profile.run('solveproblem()')

'''
#notes from forum: "remove all numbers where 2,4,6,8,0,5 occured." 
because the rotation of this cannot be a prime
'''

 