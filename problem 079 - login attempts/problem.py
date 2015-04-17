# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator
"""

import profile
from numpy import loadtxt

filename = "p079_keylog.txt"

def read_file(filename):
    substrings = loadtxt(filename, dtype = bytes).astype(str)  
    return substrings
    



def solve_problem():
    substrings = read_file(filename)
    possible_codes = []
    
    return 0
    

solve_problem()    
# profile.run('solve_problem()')   