# -*- coding: utf-8 -*-
"""
Created on Wed Jan 08 16:53:44 2014

@author: gruenewa
"""

import math

def generate_primes(max_prime):
    #liste von ungeraden zahlen, die potentiell prime sind
    #boolean liste, dessen index mit der primzahl verknüpft ist und
    #boolean = true = prime
    #index=(zahl-3 / 2)
    #0=3
    #1=5       
    #2=7
    #
    #zahl=index*2+3
    def to_index(number):
        return (number-3)//2
    
    def to_number(index):
        return index*2+3
        
    primes = [False]*to_index(max_prime)

    index = 0    
    while index < len(primes):
        
        index +=1
        
    return 0

#this seve seems way to complex, so i build an easier one with less index-number conversion

def solveproblem():

    
    
    return 0
    
    
solveproblem()    