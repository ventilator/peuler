# -*- coding: utf-8 -*-
"""
Created on Mon Apr 08 21:03:48 2013

@author: Der_Ventilator

n  n/2 (n is even)
n  3n + 1 (n is odd)
"""


"""
minstartingnumber = 1

maxfoundlength = 1

maxstartingnumber = 999999

def nextcollatz(n): 
    if n % 2 == 0:
        return n // 2
    else:
        return 3*n + 1
        
        
for startingnumber in range(minstartingnumber,maxstartingnumber+1):
    currentnumber = startingnumber
    currentlength = 0
    
    while currentnumber != 1:
        currentnumber = nextcollatz( currentnumber )            
        currentlength += 1
        
    if currentlength > maxfoundlength:
        maxfoundlength = currentlength
        print startingnumber, maxfoundlength

#after 2 min 837799 524, correct result

"""

"""
Optimierung:
    Nur noch Sequencen durchgehen, die nicht schonmal in einer Längeren enthalten waren

"""


minstartingnumber = 1

maxfoundlength = 1

maxstartingnumber = 999999

#leere Liste mit den Elementen für später
listofpassednumbers = []

def nextcollatz(n): 
    if n % 2 == 0:
        return n // 2
    else:
        return 3*n + 1
        
        
for startingnumber in range(minstartingnumber,maxstartingnumber+1):
    #wenn die startingnumber nicht in der Liste, Überprüfe sequence
    if startingnumber not in listofpassednumbers:
        currentnumber = startingnumber
        currentlength = 0
        
        while currentnumber != 1:
            currentnumber = nextcollatz( currentnumber )
            # füge current number einer Liste hinzu  (wenn nicht schon drin)            
            if currentnumber not in listofpassednumbers:
                listofpassednumbers.append( currentnumber )
                               
            
            currentlength += 1
            
        if currentlength > maxfoundlength:
            maxfoundlength = currentlength
            print startingnumber, maxfoundlength
            
#well, das Programm wird dadurch noch langsamer