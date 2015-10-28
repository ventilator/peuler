# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 17:33:13 2015

@author: venti



The first known prime found to exceed one million digits was discovered in 1999, and is a Mersenne prime of the form 26972593−1;
 it contains exactly 2,098,960 digits. Subsequently other Mersenne primes, of the form 2p−1, have been found which contain more digits.

However, in 2004 there was found a massive non-Mersenne prime which contains 2,357,207 digits: 28433×2^7830457+1.

Find the last ten digits of this prime number.

"""

# prime = 28433 * 2**7830457 + 1
exponent = 7830457

factor = 2
scale = 28433
addition = 1
cutoff = 10**12 # store only last 12 digits during computation


# debug values
#exponent = 100
#scale = 1
#addition = 0

prime = 1
prime *= scale

for i in range(exponent):
    prime *= 2
    prime = prime % cutoff
    
prime += addition  


str_prime = str(prime)
print("solution:")
print(str_prime[-10:])

#solution: 8739992577



# there is an efficient pow function which can do the cutoff automatically:

# print ((28433*pow(2,7830457,10**10)+1)%(10**10))