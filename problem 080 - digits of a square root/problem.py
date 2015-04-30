# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:14:23 2015

@author: gruenewa


It is well known that if the square root of a natural number is not an integer, then it is irrational. 
The decimal expansion of such square roots is infinite without any repeating pattern at all.

The square root of two is 1.41421356237309504880..., and the digital sum of the first one hundred decimal digits is 475.

For the first one hundred natural numbers, find the total of the digital sums of the first one hundred decimal digits 
for all the irrational square roots.

"""
from decimal import *
getcontext().prec = 110 # max 10 before comma, 100 after comma


def get_sum_of_decimal_digits(number, digits):
    str_number = str(number)
    if str_number.find(".") == -1:
        return 0    
    
    sum_of_digits = 0
    for i, digit in enumerate(str_number):
        if (i < digits):
            if (digit == "."): # if decimal point, do not calc sum but increment counter boundary by 1 to account for "."
                digits += 1
            else:                
                sum_of_digits += int(digit)
    return sum_of_digits


print("ready:", get_sum_of_decimal_digits(Decimal(2).sqrt(), 100) == 475)
    
total_sum = 0
max_number = 100
digits_to_sum = 100

for i in range(1, max_number + 1):
    sum_of_decimal_digits = get_sum_of_decimal_digits(Decimal(i).sqrt(), digits_to_sum)
    print(i, sum_of_decimal_digits)    
    total_sum = total_sum + sum_of_decimal_digits
    
print(total_sum)    

"""
alternative: 
http://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Digit-by-digit_calculation

implemented by hand once, but not in code since Decimal() lib came around

short solution from forum:

from decimal import *
getcontext().prec=102
print sum([sum([int(j) for j in str(Decimal(i).sqrt()/10)[2:102]]) for i in range(2, 100)])-sum(range(2,10))
"""