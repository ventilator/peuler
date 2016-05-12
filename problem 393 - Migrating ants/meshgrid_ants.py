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
    

def init_meshgrids():
    # generate two mesh grids. They contain all datapoints 
    Y, X = np.mgrid[-1:-dim_y:dim_y*1j, 1:dim_x:dim_x*1j]
    U = np.zeros([dim_y, dim_x])
    V = np.zeros([dim_y, dim_x])
    return X, Y, U, V
    

def legal_sequence(U, V, field):
    
    def momentum_converved(A):
        if sum(sum(A)) == 0:
            return True
        else:
            return False
            
    def rows_are_conserved(A):
        for row in A:
            if (sum(row)) != 0:
                return False
        return True        
        
            
    # 1) must not move out of boundary
    
    # 2) must not move to place which is already populated
    
    # 3) must not swap places
    
    # 1) and 2) are the same --> sum of a row/col has to be constant
    # if total sum of U or V are not 0, netto movement has occured
    # still out of boundary problem: e.g. if all move to the outside 
    # then momentum is convserved and still sum == 0
    if momentum_converved(U) and momentum_converved(V):
        return_flag = True
    else:
        return_flag = False # could directly return False
        
    # check if ants sit on top of each other    
    if rows_are_conserved(field) and (rows_are_conserved(np.transpose(field))):
        return_flag = True
    else:
        return_flag = False        
    

    # check for step 3) is a bit tricky. Essentially we could check, if two
    # vectors from neightbours cancel each other. Or each ant could take
    # something (unique) along which may not be brought back to its origin, 
    # e.g. an increasing number. and if in the end there is a field position,
    # which is 0, then there was a swapping of places
    
    return return_flag


def iterate_over_each(X, Y, U, V, ants, movement_sequence, field, traceing_field):
    step = 0

    # iterate over each koordinate and apply a particular movement sequence
    for y in range(len(X)):
        for x in range(len(X[y])):
            # print(X[y, x], Y[y, x])
            u = movement_sequence[step][0] # movement in x direction
            v = movement_sequence[step][1] # movement in y direction
            U[y, x] = u 
            V[y, x] = v                
            field[y, x] -= 1 # ant walks away

            # field: prevents two ants on the same field            
            
            # check if target movement vector + source vector cancel each other
            # this would mean, swapping was here
            if (0 <= (y-v) < dim_y) and (0 <= (x+u) < dim_x):
                if ((U[y, x] + U[y-v, x+u]) == 0) and ((V[y, x] + V[y-v, x+u]) == 0):
                    #swapping
                    return False
            

            if (0 <= (y-v) < dim_y) and (0 <= (x+u) < dim_x):
                field[y-v, x+u] += 1 # ant comes here

                        
            else:
                return False
            step += 1

    return True


def iterate(ants):
    # generate all possible sequences of movement
    movement_sequences = itertools.product(directions, repeat=max_steps)    
    testbreaker = 0       
    
    for i, movement_sequence in enumerate(movement_sequences):
        X, Y, U, V = init_meshgrids()
        field = ants.copy()
        traceing_field = ants.copy() # ants record steps and take them with them
        if i == 64618 or i == 64618 or True: #print only one specific solution
            if iterate_over_each(X, Y, U, V, ants, movement_sequence, field, traceing_field):
                   
                if legal_sequence(U, V, field):
                    plot(X, Y, U, V)
                    print("sequence id: ", i)
#                    print("U")
#                    print(U)
#                    print("V")
#                    print(V)
                    testbreaker += 1                
                
            if testbreaker > 10: break  

    print("found solutions: ", testbreaker)      
        

dim_x = 4
dim_y = 2
max_steps = dim_x*dim_y
up = np.array([0,-1])
down = np.array([0,1])
left = np.array([-1,0])
right = np.array([1,0])
directions = [up, down, left, right]
start_point = np.array([0,0])
total_steps = 0




ants = np.zeros([dim_y, dim_x])
#print("U")
#print(U)

# plot(X, Y, U, V)

iterate(ants)
## plot all pairs
#print("x y")
#for col,row in zip(X,Y):
#    for x,y in zip(col,row):
#        print(int(x),int(y))