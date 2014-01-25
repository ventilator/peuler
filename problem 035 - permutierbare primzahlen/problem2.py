# -*- coding: utf-8 -*-
"""
Created on Wed Jan 08 16:53:44 2014

@author: gruenewa
"""

import math

def generate_primes(max_prime):
    #liste von (ungeraden zahlen), die potentiell prime sind
    #boolean liste, dessen index mit der primzahl verknüpft ist und
    #boolean = true = prime
    #index = number

    primes = [True]*(max_prime+1)
    
    #list, which will contain the primes as numbers
    listofprimes = [2] 

    #indices are noted in the form i=prime, so the list start with number 0
    #2,3 are a prime
    #even numbers are ignored by default except number 2, they are never prime
    #sieve starts at 3

    
    #sieve
    index = 3    
    while index < len(primes):
        if primes[index]:            
            listofprimes.append(index) #convert sieve to list of primes
            product = index*index #begin with prime² (optimization)
            while product < len(primes):
                primes[product] = False #set nonprimes to False
                product += index #increase product by one factor                
        index +=2 #ignore even numbers
    #sieve ends

      
        
    return listofprimes

#this seve seems way to complex, so i build an easier one with less index-number conversion

def solveproblem():
    primes = generate_primes(20)
    print primes
    
    
    return 0
    
    
solveproblem()    