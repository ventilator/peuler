# -*- coding: utf-8 -*-
"""
Created on Sat May 04 15:09:48 2013

@author: ventilator
"""
starti = 2
stopi  = 1000
#stopi  = 10


#punkt im pattern, an dem angefangen wird zu suchen
#ab da sollte es bereits regelmäßig sein
startdigit = 30
#untersuchbare laenge
digits = stopi*2 + startdigit + 1



#maximal findbare laenge (rest kann nicht länger als nummer selbst sein)
laenge = stopi

#maxj
maxj = 1


#using the int package to get as many digits as i want to
for i in range(starti,stopi+1):
    fraction = str(10**digits / i)

    
    j = 1

    while fraction[startdigit:startdigit+laenge] != fraction[startdigit+j:startdigit+laenge+j]:
        j += 1
        if j == laenge: break

    if j > maxj:    
        #print "{:3}".format(i), fraction, j, fraction[startdigit:startdigit+j]  
        print "{:3}".format(i), j, fraction[startdigit:startdigit+j]         
        maxj = j

#gives correct answer of 983 in 1sec