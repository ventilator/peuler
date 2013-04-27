# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 15:17:14 2013

@author: ventilator
"""

def splitnumberintodigits( num ):
    listofliterals = []
    
    if num > 0:
    
        i = 1
        while num // i != 0:
            digit = num % (i * 10)
            
            
            #print num, digit
            num = num - digit
            listofliterals.append( digit // i )
            #print num
            
            i = i * 10
            listofliterals.reverse
    elif num == 0:
        listofliterals.append ( 0 )
    else:
        # 'not a positive number'
        listofliterals = splitnumberintodigits ( num * -1 )
    
    return listofliterals


nmax = 100    
product = 1

n = nmax
while n > 0:
    product = product * n
    n = n - 1    

productlist = splitnumberintodigits( product )

summe = 0
for i in productlist:
    summe += i
    
print summe   

#testing
print map(int,str(1234))
print sum(productlist) 
        