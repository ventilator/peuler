# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator
"""

'''

worst brute force ever. do not even look at this. there are very neat versions
in the forum

'''

import profile

pandigital_set = set(['1','2','3','4','5','6','7','8','9'])
max_found = 0

# info: this function is shit. look at problem 41 for a better one
def check_for_pandigitalism(number):
    global max_found
    result = False
    
    str_number = number
    set_number = set()
    for char in str_number:
        set_number.add(char)
    
    #print set_number    
    #print pandigital_set
    
    if (set_number == pandigital_set) and (len(number)==9):
        result = True
        print 'one candiadte: ' + number
        
        if int(number) > max_found:
            max_found = int(number)
    
    return result
    

#def check_for_double_digit(number):
    
        
    

def solve_problem():
    #print check_for_pandigitalism(192384576)
    
    for testnumber in range(1,100000):
        pandigital_candidate = ''
        #pandigital_candidate_number = 0
        multi = 1
        #print 'testing ' + str(testnumber)
        
        while (not check_for_pandigitalism(pandigital_candidate)) and len((pandigital_candidate))<=9:
            pandigital_candidate += str(testnumber*multi)
            multi += 1
            #print pandigital_candidate
            
     
            
        
    print 'max candidate : ' + str(max_found)
    return 0
    
    
profile.run('solve_problem()')   
#profile.run('check_for_pandigitalism(192384576)')
