# -*- coding: utf-8 -*-
"""
Created on Mon May 20 00:27:37 2013

@author: ventilator
"""
#Timing
import time

timing_program_start = time.clock()
timing_start = time.clock()

def printtime(reason):
    global timing_start
    if reason == "total":
        global timing_program_start
        timing_start = timing_program_start
        print '---total---'
        reason = 'End of calculation.'
    print 'The execution took {time:.3f}s. {reason}'.format(time = (time.clock() - timing_start), reason=reason)
    timing_start = time.clock()
    
#Timing end.    
'''
#max coins = 200 of 1
100 of 2
40 of 5


2
1 1 
1 50 50
50 50 50 50 
.
.
.
.
1 .. 1

ununterscheidbare, ungeordnete Kombinatorik
n über k: Binomialkoeffizient von 200 aus 8 (ziehen mit zurücklegen) = 10^13 Möglichkeiten zu Kombinieren


1) lege münze auf tisch
2) schaue nach, ob münzhaufen = 2€
3) wenn nicht, lege noch eine münze auf tisch
'''
import matplotlib.pyplot as plt

sumtocombine = 200
count = 0
numberofcompletedicts = 0

valueofcoins = [100, 50, 20, 10, 5, 2, 1]
'''
there is only one way to use the 200 coin, so i will exclude this from calculations
'''
numberofcoins = 0,0,0,0,0,0,0
numberofcompletedicts +=1
arrayofdicts = set()
arrayofdicts.add(numberofcoins)

completedstacks = set()

#calculate key*value = stored money
def moneyontable(adict):
    summe = 0
    global valueofcoins
    for i in range(len(valueofcoins)):
        summe += adict[i]*valueofcoins[i]

    return summe    

'''
nimmt arrayofdicts
addend jeweils eine münze zu jedem dict
wenn dict vollständig, dann print
wenn nicht, zu neuem array hinzufügen
'''
'''
neuer plan: münzsammlungen werden in sets gespeichert-> jede sammlung gibt es automatisch nur einmal
eine münzsammlung ist ein tuple. das kann zwar nur über den umweg einer Liste geändert werden,
kann aber in sets eingefügt werden, da hashable5



übrigens: mit tuples ins arrays dauert die berechnugn von 350.000 möglichkeiten 46 sekunden.
das ergebnis ist aber inkorrekt.
schade
mit der nativen vermeidung von array uns dem usen von sets: auch 45 sekunden. innerhalb der messgenauigkeit
'''

def addacoin(arrayofdicts):

    newarray = set()
    global sumtocombine
    global completedstacks

    for adict in arrayofdicts:
        for akey in range(len(adict)):
            newlist = list(adict[:])
            newlist[akey] += 1
            newdict = tuple(newlist)

  
            sumofnewdict = moneyontable(newdict)
            if sumofnewdict < sumtocombine:
                #if newdict not in newarray is obayed by using a dict
                newarray.add(newdict)
            if sumofnewdict == sumtocombine:
                #you cannot just count here, because in one round there are the same stacks finished, which just took a differen way
                completedstacks.add(newdict)

    return newarray           







iterationcomplete = []
iterationpending = []
rounds = 0

while len(arrayofdicts) > 0:
    rounds += 1
    arrayofdicts = addacoin(arrayofdicts)
    numberofcompletedicts = len(completedstacks) +1 #+1 for the 2pound coin
    iterationcomplete.append(numberofcompletedicts)
    iterationpending.append(len(arrayofdicts))
    
    print "complete: ", numberofcompletedicts, "remaining: ",len(arrayofdicts)
    printtime("complete round {}".format(rounds))


print "total combinations:"
print numberofcompletedicts

plt.plot(iterationcomplete)
plt.plot(iterationpending)
plt.show()
  
printtime("total")    