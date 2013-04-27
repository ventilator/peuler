# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 15:51:34 2013

@author: ventilator
"""

#find all divisors
def divisorsofnumber ( num ):
    divisors = []
    for i in range(1,num // 2 +1):
        if num % i == 0:
            divisors.append (i)
    return divisors
    
    
    
divisorlist = divisorsofnumber(20)    
#print divisorlist

summe = sum(divisorlist)
#print summe

listofsumofdivisors = []

nmax = 10000

for i in range(1,nmax+1):
    listofsumofdivisors.append(sum(divisorsofnumber(i)))
#print listofsumofdivisors
    
#print listofsumofdivisors     

#print sum(divisorsofnumber(220))
listofamicable = []

for i,d in enumerate(listofsumofdivisors):
    # i = zahlA zB 220
    # d = teilerA zB 284
    # überprüfe ob d(284) = listofsumofdivisors[d-1], also der teilerB der zahlB=teilerA
    # gleich der zahlA entspricht = i+1
    #
    #
    #
    if d<nmax and listofsumofdivisors[d-1] == i+1 and i+1 != d:
        #print i+1,d
        listofamicable.append(i+1)

print listofamicable   
print sum(listofamicable) 