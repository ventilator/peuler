# -*- coding: utf-8 -*-
"""
Created on Mon May 20 00:27:37 2013

@author: ventilator
"""
#Timing
import time

timing_start = time.clock()

def printtime(reason):
    global timing_start
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
#virtual 0cent coin
#coins        = [200,100,50,20,10,5,2,1]
#numberofcoin = [1,2,4,10,20,40,100,200]
#coins.reverse

#combination = [0]*200

#calculate key*value = stored money
def moneyontable(adict):
    summe = 0
    for key in adict:
        summe += key*adict[key]
        #print key, adict[key]
    #print summe
    return summe    

'''
nimmt arrayofdicts
addend jeweils eine münze zu jedem dict
wenn dict vollständig, dann print
wenn nicht, zu neuem array hinzufügen
'''


def addacoin(arrayofdicts):
    #global coins
    newarray = []
    global numberofcompletedicts

    for adict in arrayofdicts:
        #print adict
        for akey in adict.iterkeys():
            newdict = adict.copy()            
            newdict[akey] += 1
            sumofnewdict = moneyontable(newdict)
            if sumofnewdict < sumtocombine:
                if newdict not in newarray:
                    newarray.append(newdict)
            elif sumofnewdict == sumtocombine:
                numberofcompletedicts += 1
                #print "winner", sumofnewdict, newdict, numberofcompletedicts
            #print newdict
        #print newarray   
    return newarray            


dictofcoins = {200:0, 100:0, 50:0, 20:0, 10:0, 5:0, 2:0, 1:0}
'''
there is only one way to use the 200 coin, so i will exclude this from calculations
'''
dictofcoins = {100:0, 50:0, 20:0, 10:0, 5:0, 2:0, 1:0}
numberofcompletedicts +=1
''' '''

#dictofcoins = [0]*6
#arrayofdicts  = [dictofcoins]
arrayofdicts = []
arrayofdicts.append(dictofcoins)

'''cannot use sets, cause i want to change content, so they are not hashable'''

#print dictofcoins
iterationcomplete = []
iterationpending = []

while len(arrayofdicts) > 0:
    arrayofdicts = addacoin(arrayofdicts)
#print arrayofdicts
    iterationcomplete.append(numberofcompletedicts)
    iterationpending.append(len(arrayofdicts))
    
    #plt.plot(iterationcomplete,iterationpending)
    #plt.show()
    
    print "complete: ", numberofcompletedicts, "remaining: ",len(arrayofdicts)
    printtime("complete a round")
#print arrayofdicts

#setofcoins = set([1]) 
#arrayofsetofcoins = []
#for c in coins:
    #arrayofsetofcoins.append(set([c]))
    
#print arrayofsetofcoins  
#addacoin(arrayofsetofcoins)       
#print count            