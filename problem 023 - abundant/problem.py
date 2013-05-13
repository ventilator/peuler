# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 11:40:04 2013

@author: ventilator
"""
import time
timing_start = time.clock()


#find all divisors of a number
#ver 2
#this should be pushed into a lib
def divisorsofnumber( num ):
    divisors = []
    for i in range(1,num // 2 +1):
        if num % i == 0:
            divisors.append (i)
    return divisors
    
 

#print  sum(divisorsofnumber(28123))   #is a prime number
    
starti = 1
stopi  = 28123
#stopi  = 60
abundatnumbers = []


#this gives a list of abundat numbers
for i in range(starti,stopi+1):
    if sum(divisorsofnumber(i)) > i:
        abundatnumbers.append(i)
#it takes 13 seconds and gives you 6965 numbers


#print abundatnumbers[-1] (last number is 28122)


print 'The execution took {time:.3f} s. (find all abundat numbers)'.format(time = (time.clock() - timing_start))   
timing_start = time.clock()

#find all possible sums and add them to a list
#this takes ages. hm.
sumsofabundatnumbers = []

for i in abundatnumbers:
    #better: j = i...max, not j = 0..max)
    for j in abundatnumbers:
        summe = i + j
        if summe > stopi: #> oder >= ?
            break
        #next step omitted, so it takes 8s instead of >100
        #if summe not in sumsofabundatnumbers:  
        sumsofabundatnumbers.append(summe)
            
#gives 24.294.140 numbers  
            

print 'The execution took {time:.3f} s. (make a list of its sums)'.format(time = (time.clock() - timing_start))   
timing_start = time.clock()

#print len(sumsofabundatnumbers) 
sumsofabundatnumbers.sort()
#takes 5s to sort this
print 'the first sum is {}, the last is {}.'.format(sumsofabundatnumbers[0],sumsofabundatnumbers[-1])

print 'The execution took {time:.3f} s. (sort this list)'.format(time = (time.clock() - timing_start))   
timing_start = time.clock()



'''
noduplicatesofsumofabundatnumbers = []

#0 has not to be in the list
currentabundat = 0

#using the fact, that it is a sorted list
#so i dont have to use timeconsuming "i in list" commands
for i in noduplicatesofsumofabundatnumbers:
    if currentabundat != i:
         noduplicatesofsumofabundatnumbers.append(i)
         currentabundat = i
         

print 'The execution took {time:.3f} s. (delete all duplicates)'.format(time = (time.clock() - timing_start))   
timing_start = time.clock()
'''
      
      
#print abundatnumbers            
#print sumsofabundatnumbers     
#print notasumofabundatnumbers

#print '{} nonduplicates found'.format(len(noduplicatesofsumofabundatnumbers))   

notasumofabundatnumbers = []
for i in range( starti, stopi+1):
    notasumofabundatnumbers.append(i)
    

for i in sumsofabundatnumbers:
    #delete all sumsofabundatnumbers
    #1 is on arrayposition 0
    notasumofabundatnumbers[ i-1 ] = 0
    


print 'Solution: {}'.format(sum(notasumofabundatnumbers)   )


print 'The execution took {time:.3f} s.'.format(time = (time.clock() - timing_start))   
