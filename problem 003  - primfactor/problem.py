# -*- coding: utf-8 -*-


#x = 13195
x = 600851475143 
divisor = 2

while divisor < x:

    while x % divisor != 0:
        divisor = divisor + 1
    
    print 'Primfaktor: ' + str(divisor)
    x = x / divisor
    print 'Rest: ' + str(x)