# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 22:00:56 2014

@author: ventilator
"""
import collections

#123 -> set([312, 123, 231])
def give_rotations_of_number(number):
    collection_of_number = collections.deque(str(number))
    rotated_numbers = set()

    for x in range(0,len(str(number))):
        rotated_numbers.add(int(''.join(map(str,(list(collection_of_number))))))
        collection_of_number.rotate(1)

    return rotated_numbers
        
    