# -*- coding: utf-8 -*-

summe = 0
#Startwerte
zahl1 = 1
zahl2 = 2
zahl3 = 0
maxzahl = 4000000







while zahl2 < maxzahl:
        #wenn gerade
    if zahl2 % 2 == 0:
        summe = summe + zahl2
        
    zahl3 = zahl1 + zahl2
    zahl1 = zahl2
    zahl2 = zahl3
    #print zahl3

            
print summe
