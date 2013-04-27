# -*- coding: utf-8 -*-
"""
Created on Mon Apr 01 13:44:35 2013

@author: ventilator
"""

#zähle zahlen und prüfe auf teilbarkeit
#wenn nicht teilbar -> prim
#zähle primzahlen


untersuchtezahl = 3
startdivisor = 2
divisor = 2
maxgefundene = 10001

#wegen der 2
anzahlgefundene = 1

while anzahlgefundene <= maxgefundene:
    prime = True
    
    #größter teiler nicht größer als haelfte oder drittel der zahl
    # eigentlich auch nicht ein viertel (da gerade) ?
    # eigentlich falsch? nur bis zum drittel checken (da gerade zahlen ausgeschlossen)
    while divisor < untersuchtezahl // 3 + 1:
        #wenn teiler gefunden, brich ab
        if untersuchtezahl % divisor == 0:
            prime = False
            break
        divisor += 1
        
    #wenn primzahl gefunden    
    if prime:
        anzahlgefundene += 1
        print untersuchtezahl
        
    #lasse die geraden zahlen aus    
    untersuchtezahl += 2
    divisor = startdivisor
    
# solution after 37sec run: 104743    