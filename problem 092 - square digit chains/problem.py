# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 16:01:33 2015

A number chain is created by continuously adding the square of the digits in a number to form a new number 
until it has been seen before.

For example,

44 → 32 → 13 → 10 → 1 → 1
85 → 89 → 145 → 42 → 20 → 4 → 16 → 37 → 58 → 89

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. 
What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?

@author: gruenewa
"""
import profile

max_number = 10**7
max_look_up_entries = 2 * max_number
lut = [None] * max_look_up_entries
# prefill with 1 and 89
lut[1] = 1
lut[89] = 89
magic_numbers = set([1,89])

def square_and_sum_digits_slow(number):
    string_number = str(number)
    final_sum = 0
    for s in string_number:
        final_sum += int(s)**2
    return final_sum


def square_and_sum_digits(number):
   final_sum = 0
   while number:
       final_sum, number = final_sum + (number % 10)**2, number // 10
   return final_sum

def sequence(start):    
    numbers_on_the_way = []
    while True:
        if lut[start] in magic_numbers:
            for number in numbers_on_the_way:
                lut[number] = lut[start]
            return lut[start]            
        numbers_on_the_way.append(start)    
        start = square_and_sum_digits(start)
            
        
def solve_problem():          
    count_1 = 0            
    for i in range(1,max_number):        
        if sequence(i) == 89:
            count_1 += 1
    print(count_1)    
    
solve_problem()   
# profile.run('solve_problem()')  

#correct answer: 8581146
