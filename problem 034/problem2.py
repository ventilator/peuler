# -*- coding: utf-8 -*-
"""
Created on Wed Jan 08 16:53:44 2014

@author: gruenewa
"""

import math
import itertools
import profile

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

    #print number, permutated_numbers
    
#    digits = split_number_into_digits(number)
 #   print digits
    #[1,2,3] -> [1,2,3],[1,3,2],[2,1,3]...
  #  print itertools.permutations('123')
   # permutated_digits = itertools.permutations(digits)
    #print permutated_digits
    #permutated_numbers = set()

  #  for numbers in permutated_digits:        
 #       permutated_numbers.add(list_of_digits_to_number(numbers))
    
    return permutated_numbers


def solveproblem():
    primes = generate_primes(100000)
    number_of_circular_primes = 4 #algorithm will not find 2,3,4 and 7
    #print primes
    #print give_unique_permutations_of_number(71)
    #copy_of_primes = primes[:]
    
    for prime in primes:
        permutated_primes = give_unique_permutations_of_number(prime)        
        permutated_primes.remove(prime) #to prevent being matched to itself
        for permutated_prime in permutated_primes:
            counter = 0            
            if permutated_prime in primes:
                #primes.remove(permutated_prime)
                number_of_circular_primes += 1 #this values is grater 100.000? cannot be the case
                counter += 1
                #print 'hurrra', prime, permutated_prime
            if counter > 2:
                print counter #is there a tripplet?
        #copy_of_primes.remove(prime)        
        #print prime
        
    
    
    print 'number_of_circular_primes', number_of_circular_primes
    return 0
    
profile.run('solveproblem()')
 