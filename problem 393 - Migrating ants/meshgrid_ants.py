# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:41:36 2016

@author: gruenewa
"""
# use meshgrids
# create vector field with positions of ants (2 meshgrids X Y)
# create vector field with movement vectors of ants (2 meshgrids U V)
# addition of position and movement creates new state of ants

# working with meshgrids: iterate over all contents (use zip funktion)
# neightbours should be also the same as in a conventional cartesian grid
import numpy as np
import itertools

# for plotting
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt

import time
start_time = time.time()  
block_time = start_time  

def plot(X, Y, U, V):    
    plot1 = plt.figure()
    
    speed = np.sqrt(U**2 + V**2)
    plt.quiver(X, Y, U, V,          # data
               speed,               # colour the arrows based on this array
               cmap=cm.viridis,     # colour map
               headlength=5,        # length of the arrows
               scale=10.0)

    #plt.colorbar()                  # adds the colour bar    
    #plt.title('Quive Plot, Dynamic Colours')
    pts = itertools.product(X, Y)
    plt.scatter(*zip(*pts), marker='o', s=30, color='red')
    #plt.grid(plot1)
    plt.show(plot1)                 # display the plot
    
    
def plot_array(array):
    x = array
    y = [1 for _ in range(len(array))]
    array_plot = plt.figure()
    plt.plot(x, y, 'ro')
    plt.show(array_plot)
        

def init_meshgrids():
    # generate two mesh grids. They contain all datapoints 
#    Y, X = np.mgrid[-1:-dim_y:dim_y*1j, 1:dim_x:dim_x*1j]
    U = np.zeros([dim_y, dim_x])
    V = np.zeros([dim_y, dim_x])    
#    return X, Y, U, V
    return U, V
    

def legal_sequence(U, V, field):
    
    def momentum_converved(A):
        if sum(sum(A)) == 0:
            return True
        else:
            return False
            
    def rows_are_conserved(A):
        for row in A:
            if (sum(row)) != dim_x:
                return False
        return True        
        
    def cols_are_conserved(A):
        B = np.transpose(A)
        for row in B:
            if (sum(row)) != dim_y:
                return False
        return True               
    # 1) must not move out of boundary
    
    # 2) must not move to place which is already populated
    
    # 3) must not swap places
    
    # 1) and 2) are the same --> sum of a row/col has to be constant
    # if total sum of U or V are not 0, netto movement has occured
    # still out of boundary problem: e.g. if all move to the outside 
    # then momentum is convserved and still sum == 0
    
    # turns out, conversation of momentum is already covered by conservation of rows/cols in the field
#    if momentum_converved(U) and momentum_converved(V):
#        return_flag = True
#    else:
#        return False
        
        
    # check if ants sit on top of each other    
    if rows_are_conserved(field) and cols_are_conserved(field):
        return_flag = True
    else:
        return False
    

    # check for step 3) is done during generation of movement vectors.
    # if target + source == 0, then swapping occured and thus sequence is discarded

    return return_flag


def iterate_over_each(X, Y, U, V, movement_sequence, field):
    step = 0

    # iterate over each koordinate and apply a particular movement sequence
    for y in range(len(X)):
        for x in range(len(X[y])):
            u = movement_sequence[step][0] # movement in x direction
            v = movement_sequence[step][1] # movement in y direction
            U[y, x] = u 
            V[y, x] = v                
            # field: prevents two ants on the same field, evaluated later    
            # field[y, x] -= 1 # ant walks away # its to just track inflow instead of conversation of ants                   
#            if field[y, x] < -1:
#                return False
            x_u = x+u # calculate this only once, it is indeed faster by 0.5s per 25k rounds
            y_v = y-v
            if (0 <= (y_v) < dim_y) and (0 <= (x_u) < dim_x):
                field[y_v, x_u] += 1 # ant comes here  
#                if field[y-v, x+u] > 2: # more ants are already here than will walk away
#                    return False                                                      
                # check if target movement vector + source vector cancel each other
                # this would mean that swapping was here                
                if ((U[y, x] + U[y_v, x_u]) == 0) and ((V[y, x] + V[y_v, x_u]) == 0):
                    # swapping
                    return False
            else:
                # walking out of grid
                return False
            step += 1

    return True


def iterate(ants):
    # due to massive performance drop, X, Y is only generated once. No cleanup necessary        
    Y, X = np.mgrid[-1:-dim_y:dim_y*1j, 1:dim_x:dim_x*1j]    
    # generate all possible sequences of movement
    movement_sequences = itertools.product(directions, repeat=max_steps)       
    
    for i, movement_sequence in enumerate(movement_sequences):
        U, V = init_meshgrids()
        
        field = ants.copy()        
        if iterate_over_each(X, Y, U, V, movement_sequence, field):
               
            if legal_sequence(U, V, field):
                if plot_fields:
                    plot(X, Y, U, V)
                    print("sequence id: ", i)
                valid_sequences.append(i)
           
        if i % 50000 == 0:
            global block_time
            print("elapsed time: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - block_time))
            block_time = time.time()
            print("sequencing id: ", i)
            
    print("found solutions: ", len(valid_sequences))     
    print("sequence IDs of solutions")
    plot_array(valid_sequences)
        

dim_x = 4
dim_y = 4
max_steps = dim_x*dim_y
up = np.array([0,-1])
down = np.array([0,1])
left = np.array([-1,0])
right = np.array([1,0])
directions = [up, down, left, right]
start_point = np.array([0,0])
total_steps = 0
valid_sequences = []
ants = np.zeros([dim_y, dim_x])

plot_fields = True
iterate(ants)

print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))