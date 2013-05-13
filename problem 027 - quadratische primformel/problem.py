# -*- coding: utf-8 -*-
"""
Created on Sun May 12 15:50:40 2013

@author: ventilator
"""
import math

'''    
    Musterlösung

1. Make a list of all numbers from 2 to N.
2. Find the next number p not yet crossed out. This is a prime.
If it is greater than √
N, go to 5.
3. Cross out all multiples of p which are not yet crossed out.
4. Go to 2.
5. The numbers not crossed out are the primes not exceeding N


und dafür gibts noch Optimierungen wie z.B. nur die ungeraden zu kreuzen
'''

def getprimes(N):
    N += 1
    primes = [True]*(N)
    primes[0] = False
    primes[1] = False    
    #print primes
    for n,isprime in enumerate(primes):
        if isprime and n <= math.sqrt(N):
            i = 2
            while n*i < N:
                primes[n*i] = False
                i += 1
    
    integerprimes =[]            
    for n,isprime in enumerate(primes):
        if isprime:
            integerprimes.append(n)
                
    return integerprimes
    
  
    
#n² + n + 41
#n²  79n + 1601
#n² + an + b, where |a|  1000 and |b|  1000


#as for n=0 the formular gives you a prime, b has to be a prime
#b = 2..positive prime

#for n=1: 1 + a + b has to be a prime.
#max of n1 is 1 + 1000 + 1000 = 2001
#max of nx is x^2 + 1000x + 1000
#max of n2 is 4 + 2000 + 1000 = 3004
#max of n3 is 9 + 3000 + 1000 = 4009
#if I have 1.000.000 primes, I can check up to 617
#1000000 = n^2 + 1000n + 1000
#(http://www.wolframalpha.com/input/?i=1000000+%3D+n%5E2+%2B+1000n+%2B+1000)

#1st order optimization: get a list of primes 2..1000
#check all combinations for n=1

#if there are not many such combinations, brute force them till the fail to produces primes.


def getnumber(n,a,b):
    return n*n + a*n + b 
    
    
#get primes from 2..N 
primes = getprimes(1000)  
#get primes for a-loop
a1primes = getprimes(2001)
a2primes = getprimes(3004)
a3primes = getprimes(4009)
alist  = [False]*2000
offset = 1000

numberofcandidates = 0

for b in primes:
    for a in range(-1000,1001):
        n1 = getnumber(1,a,b)
        if n1 in a1primes:
            n2 = getnumber(2,a,b)
            if n2 in a2primes:
                n3 = getnumber(3,a,b)
                if n3 in a3primes:                            
                    #a, b are primes for n=0,1,2,3
                    #from here I should check if next iterations are prime and count this numbers
                    alist[a+offset] = True
                    numberofcandidates += 1
       
integeralist = []       
for a,isvalid in enumerate(alist):
    if isvalid:
        integeralist.append(a-offset)
print integeralist, len(integeralist), numberofcandidates     
           