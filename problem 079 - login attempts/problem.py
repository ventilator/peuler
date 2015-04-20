# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator



A common security method used for online banking is to ask the user for three random characters from a passcode. 
For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be: 317.

The text file, keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine 
the shortest possible secret passcode of unknown length.

"""

import profile
import itertools
from numpy import loadtxt

filename = "p079_keylog.txt"

def read_file(filename):
    substrings = loadtxt(filename, dtype = bytes).astype(str)  
    count = len(substrings)
    # unify it
    substrings=list(set(substrings))    
    count_new = len(substrings)
    print("{} duplicates removed".format(count - count_new))
    
    substrings.sort()
    return substrings
    

# checks if reply matches passcode
def match(substring, passcode):
    i = 0
    for p in passcode:
        if p == substring[i]:
            i += 1
            if i == len(substring):
                return True
    return False            


def solve_problem():
    
    substrings = read_file(filename)
    print(substrings)
    # possible_codes = [x[:] for x in [[0]*10]*10] # does the same but I dont know why
    possible_codes = [[0 for i in range(10)] for j in range(10)]
    
    for codes in substrings:
        #count first digit
        possible_codes[0][int(codes[0])] += 1
        #count last digit
        possible_codes[-1][int(codes[-1])] += 1
        #count middle digit
        possible_codes[1][int(codes[1])] += 1        
 
    print("probable begin and end of code") # does not work if two digits have same occurence
    probable_beginning = possible_codes[0].index(max(possible_codes[0]))
    probable_ending = possible_codes[-1].index(max(possible_codes[-1]))
    print(probable_beginning, probable_ending)
    
    #7 and 0 are never used in the middle and most used digit and edge, so the are at begin and end of code    
    
    for line in possible_codes:
        print(line)

    used_digits = set()
    for codes in substrings:
        for digit in codes:
            used_digits.add(int(digit))
    print("used digits in code")            
    print(used_digits)
    
    used_digits.remove(probable_beginning)
    used_digits.remove(probable_ending)
    
    for possible_passcode in itertools.permutations(used_digits):        
        str_passcode = str(probable_beginning) + "".join(str(s) for s in possible_passcode) + str(probable_ending)
        passcode_correct = True
        for code in substrings:
            if not match(code, str_passcode):
                passcode_correct = False
                break
        if passcode_correct:
            print("found one valid passcode: ")
            print(str_passcode)
    
    
    return 0
    

# solve_problem()    
profile.run('solve_problem()')  


"""
cool solution from forum:

Created a dictionary to hold which digits appeared to the left or the right of each digit. 
Once that dictionary was populated, the answer can be obtained by taking the digit with nothing to the left, 
followed by the digit with one to the left, etc.
""" 