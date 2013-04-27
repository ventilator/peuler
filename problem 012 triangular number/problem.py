# -*- coding: utf-8 -*-
"""
Created on Fri Apr 05 20:54:50 2013

@author: ventilator
"""
import math

def anzahlteiler(x):
    #sich selbst und 1 (wird später verdoppelt)
    anzahl = 0
    
    #suche zw. 1 und wurzel(x) 
    for i in range( 1, int(math.floor(math.sqrt(x))) + 1 ):
       
        if x % i == 0:
            anzahl+= 1
    
    #anzahl muss verdoppelt werden
    anzahl = anzahl * 2    
    
    #falls quadratzahl, darf quadrat nicht doppelt gezählt werden    
    #falls quadratzahl
    if int(math.ceil(math.sqrt(x))) == int(math.floor(math.sqrt(x))):
        anzahl = anzahl - 1


    
    
    return anzahl


#print  anzahlteiler(21) == 4
#print  anzahlteiler(28) == 6
#print  anzahlteiler(36) == 9

x = 1
summe = 1
gefundeneteiler = 1
maxteiler = 500
maxgefundeneanzahl = 1
stepweite = 1


while gefundeneteiler < maxteiler:
    x += 1
    summe += x
    gefundeneteiler = anzahlteiler(summe)
    

    if maxgefundeneanzahl < gefundeneteiler:
        maxgefundeneanzahl = gefundeneteiler
       # print x, maxgefundeneanzahl   
 
print x, summe, gefundeneteiler 
        
        
        