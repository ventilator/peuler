# -*- coding: utf-8 -*-

summe = 0
aktuellezahl = 0
maxzahl = 1000
divisor1 = 3
divisor2 = 5

while aktuellezahl < maxzahl-1:
    aktuellezahl = aktuellezahl + 1
    if aktuellezahl % divisor1 == 0 or aktuellezahl % divisor2 == 0:
        summe = summe + aktuellezahl
            
print summe
