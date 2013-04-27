# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 01:02:13 2013

@author: ventilator
"""

start = 999
zahl1 = start
zahl2 = start
palin = 0
maxzahl = 100
bishergroesse = 0

while zahl1 > maxzahl:
    zahl1 = zahl1 - 1
    while zahl2 > maxzahl:
        zahl2 = zahl2 - 1
        #print "1. zahl: " + str(zahl1)
        #print "2. zahl: " + str(zahl2)
        palin = zahl1 * zahl2


        if palin % (10**6) / 10**(6-1) == palin % (10**1) / 10**(1-1):
            if palin % (10**5) / 10**(5-1) == palin % (10**2) / 10**(2-1):
                if palin % (10**4) / 10**(4-1) == palin % (10**3) / 10**(3-1):

                    if palin > bishergroesse:
                        bishergroesse = palin
                        print palin
                        print "1. zahl: " + str(zahl1)
                        print "2. zahl: " + str(zahl2)                        

        
        
    zahl2 = start    

print bishergroesse    