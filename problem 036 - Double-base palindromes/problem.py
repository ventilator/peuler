# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 14:21:36 2014

@author: ventilator
"""
import profile

#base should only be 10 or 2
def isPalindrom(number,base):
    if base == 2:
        str_number = "{0:b}".format(number)
    else:    
        str_number = str(number)
    #This is extended slice syntax. It works by doing [begin:end:step]
    str_reverse = str_number[::-1]
    
    #comparing in number format to get rid of leading zeroes #by taking only odd numbers already taken into account
    #number_reversed = int(str_reverse,base)
    #print number, number_reversed, base, str_number, str_reverse, number == number_reversed
    #return number == number_reversed
    return str_reverse == str_number
    
    
def solve_problem():

    sum = 0
    #only odd number do not have a leading 0 after being reversed in binary system
    for number in range(1,1000000,2):
        #its faster (5.6sec to 2.8sec) is you compare base 10 first because of str length
        if isPalindrom(number,10) and isPalindrom(number,2):
            print number, "{0:b}".format(number)
            sum += number
            
    print "The sum of all palindromic numbers is: " + str(sum)
    return number


profile.run("solve_problem()")