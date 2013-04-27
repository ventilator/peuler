# -*- coding: utf-8 -*-


  
    

def ispalindrome( number ):
    numberstr = str(number)
    #print len(numberstr)
    palindrome = ''
    
    for k in range(1,len(numberstr)+1,1):
        #print k
        palindrome = palindrome + numberstr[-int(k)]
        
    #print 'Palindrome von ' + numberstr + ' ist ' + palindrome    
        
    
    
    palindrome = int(palindrome)
    
    
    result = number == palindrome
    return result
    
    
maxvalue = 999
imax = maxvalue
jmax = maxvalue
maxpalindrome = 0

for i in range(imax,1,-1):
    
    for j in range (jmax,1,-1):
        #print i,j,i*j
        if ispalindrome (i*j):
           if maxpalindrome < i*j:
               maxpalindrome = i*j
           
           #break
       
print 'Großes Palindrom: ' + str(maxpalindrome)       