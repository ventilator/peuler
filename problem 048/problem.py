# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:39:28 2015

@author: gruenewa



The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.

"""


def main():
    max_i = 1000
    series_sum = 0
    for i in range(1,max_i+1):
        series_sum += i**i
        
    print(max_i, series_sum, str(series_sum)[-10:])        


import cProfile
cProfile.run('main()') 