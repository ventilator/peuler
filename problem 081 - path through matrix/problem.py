# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:06:16 2015

@author: gruenewa



In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by only moving to the right and down, 
is indicated in bold red and is equal to 2427.
⎛⎝⎜⎜⎜⎜⎜⎜131201630537805673968036997322343427464975241039654221213718150111956331⎞⎠⎟⎟⎟⎟⎟⎟

Find the minimal path sum, in matrix.txt, a 31K text file containing a 80 by 80 matrix, 
from the top left to the bottom right by only moving right and down.

"""
import numpy as np

max_x = 79
max_y = max_x
start_x = max_x
start_y = max_y
filename = "p081_minimatrix.txt"

def read_file(filename):
    f = open(filename,'r')
    raw_content = []

    for line in f:
        raw_content.append(line.rstrip('\r\n').split(","))
    
    f.close()   
    
    # print(raw_content) 
    # convert everything to int
    raw_content = list(list(map(int,lines)) for lines in raw_content)
    
    return raw_content 
    
#    content = []
#    for line in raw_content:
#        content.append(line.split(","))
#        
#    
#    print(content)
    
def give_neightbours(x, y, mode=["top", "left"]):
    return 0
    

def diagnonal_walk(content):
    # we will begin at bottom right and walk diagonally to top left
    lines, rows = content.shape
    print("lines, rows")
    print(lines, rows)
    
    
    
    
def solve_problem():
    # read file
    content = read_file(filename)
    # convert to 2D array from numpy
    content = np.array(content)
    print("original matrix")
    print(content)
    diagnonal_walk(content)

    return 0


solve_problem()    