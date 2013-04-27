# -*- coding: utf-8 -*-
"""
Created on Mon Apr 01 13:44:35 2013

@author: ventilator
"""
import math
#adaption von problem 7
#zähle zahlen und prüfe auf teilbarkeit
#wenn nicht teilbar -> prim
#addiere primzahlen


untersuchtezahl = 3
startdivisor = 2
divisor = 2

#wegen der 2
gesamtsumme = 2
maxzahl = 2000000


while untersuchtezahl < maxzahl:
    prime = True
    
    #wenn es einen teiler größer als die wurzel gibt,
    #gibt es auch einen kleiner als die wurzel.
    #also nur bis zur wurzel suchen
    while divisor <= math.sqrt(untersuchtezahl):
        #wenn teiler gefunden, brich ab
        if untersuchtezahl % divisor == 0:
            prime = False
            break
        #hm nur gerade zahlen sind durch gerade teilbar, daher jeden zweiten Teiler auslassen?
        #aber was wenn derjeniger, der größer als wurzel(zahl) ungerade ist?
        divisor += 1
        
    #wenn primzahl gefunden    
    if prime:
        gesamtsumme += untersuchtezahl

        
    #lasse die geraden zahlen aus   
    #geraden zahlen kein prim
    untersuchtezahl += 2
    divisor = startdivisor
    
# solution after 1:12sec run: 142913828922 - algorithmus eigentlich zu lang    
print untersuchtezahl, gesamtsumme


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