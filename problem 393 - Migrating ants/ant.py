# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:01:19 2016

@author: noob
"""
import numpy as np
x = 4
y = 2
max_steps = x*y

up = np.array([0,-1])
down = np.array([0,1])
left = np.array([-1,0])
right = np.array([1,0])
directions = [up, down, left, right]
start_point = np.array([0,0])
total_steps = 0

def move(start, direction, field, step):
    target = start + direction
    tx = target[0]
    ty = target[1]
    if (0 <= tx < x) and (0 <= ty < y) and (field[ty, tx] == 0):
        field[ty, tx] = step
        legal = True
    else:
        legal = False
    return legal, field
    

def iterate():
    field = np.zeros([y,x])
    step = 1
    next_step(field.copy(), start_point, step)
    
def next_step(field, position, step):
    global total_steps
    total_steps += 1
    
    for direction in directions:        
        legal, field = move(position, direction, field, step)    
        if legal:             
            if step < max_steps:
                next_step(field.copy(), position + direction, step+1)
            else:                
                print(field)
    
    
    
iterate()
print("total iterations", total_steps)