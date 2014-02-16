# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 22:00:56 2014

@author: ventilator
"""
import collections

#123 -> set([312, 123, 231])
def give_rotations_of_number(number):
    collection_of_number = collections.deque(str(number))
    rotated_numbers = set()

    for x in range(0,len(str(number))):
        rotated_numbers.add(int(''.join(map(str,(list(collection_of_number))))))
        collection_of_number.rotate(1)

    return rotated_numbers
        

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