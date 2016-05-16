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


# note: 4x4 grid would mean there are >4*10^9 sequences. 
# since I need 4s per 100k sequences -> 48h per run.
# after some delicate adjustment on sequence generation, one should not check
# more than 165.636.900 sequences.


import numpy as np
import itertools
import operator
import sys

# for plotting
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt

import time
start_time = time.time()  
block_time = start_time  

dim_x = 4
dim_y = 2
max_steps = dim_x*dim_y
# hm, store directions in an hashable, immutable, ordered object (tuple)
#up = np.array([0,-1])
#down = np.array([0,1])
#left = np.array([-1,0])
#right = np.array([1,0])
# vectors are tuples -> hashable, immutable
up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)
directions = [up, down, left, right]
positive_directions = [up, right]
negative_directions = [down, left]

start_point = np.array([0,0])
total_steps = 0
valid_sequences = []
ants = np.zeros([dim_y, dim_x])

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
#    U = np.zeros([dim_y, dim_x])
#    V = np.zeros([dim_y, dim_x])  
    U = ants.copy() # a bit faster (20%)
    V = ants.copy()
#    return X, Y, U, V
    return U, V
    
# as it turns out, e.g. on 2x4 field this will only be called 80 times out of 65k (outdated information)
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
#    if rows_are_conserved(field) and cols_are_conserved(field):
#        return_flag = True
#    else:
#        return False
    return_flag = True     
    for y in field:
        for x in y:
            if x != 1:
                return False

    # check for step 3) is done during generation of movement vectors.
    # if target + source == 0, then swapping occured and thus sequence is discarded

    return return_flag


def iterate_over_each(X, Y, U, V, movement_sequence, field):
    def check_boundary(x,y):
        return (0 <= y < dim_y) and (0 <= x < dim_x)
    
    step = 0
    # iterate over each koordinate and apply a particular movement sequence
    for y in range(dim_y): #hardcoded dim_? instead of len(), because faster
        for x in range(dim_x):
            u = movement_sequence[step][0] # movement in x direction
            v = movement_sequence[step][1] # movement in y direction
              
            # field: prevents two ants on the same field, evaluated later    
            # field[y, x] -= 1 # ant walks away # its to just track inflow instead of conservation of ants                   
#            if field[y, x] < -1:
#                return False
            x_u = x+u # calculate this only once, it is indeed faster by 0.5s per 25k rounds
            y_v = y-v
            if (0 <= (y_v) < dim_y) and (0 <= (x_u) < dim_x):
                # check if target movement vector + source vector cancel each other
                # this would mean that swapping was here                
                if ((u + U[y_v, x_u]) == 0) and ((v + V[y_v, x_u]) == 0):
                    # swapping
                    return False
                    
                field[y_v, x_u] += 1 # ant comes here  
#                if field[y-v, x+u] > 2: # more ants are already here than will walk away
#                    return False                                                      

            else:
                # walking out of grid
                return False
                
            U[y, x] = u 
            V[y, x] = v                  
                
            step += 1

    return True

"""
* sequences have to conserve total momentum: sum(sequence) == 0
* this implies during generation for each movement vector an inverse vector has to be inserted
* this can be used in sequence generations: as many ups as downs and as many lefts as rights
* but careful: number of ups is not equal number of rights
* so I could generate a sequence from only ups ... up to only rights. Then invert this list add counter vectors.
* then permutate each of this lists, then test all of them
"""

# help from http://stackoverflow.com/questions/12836385/how-can-i-interleave-or-create-unique-permutations-of-two-stings-without-recurs/12837695#12837695
def unique_permutations(seq):
    """
    Yield only unique permutations of seq in an efficient way.

    A python implementation of Knuth's "Algorithm L", also known from the 
    std::next_permutation function of C++, and as the permutation algorithm 
    of Narayana Pandita.
    """

    # Precalculate the indices we'll be iterating over for speed
    i_indices = range(len(seq) - 1, -1, -1)
    k_indices = i_indices[1:]

    # The algorithm specifies to start with a sorted version
    seq = sorted(seq)

    while True:
        yield seq

        # Working backwards from the last-but-one index,           k
        # we find the index of the first decrease in value.  0 0 1 0 1 1 1 0
        for k in k_indices:
            if seq[k] < seq[k + 1]:
                break
        else:
            # Introducing the slightly unknown python for-else syntax:
            # else is executed only if the break statement was never reached.
            # If this is the case, seq is weakly decreasing, and we're done.
            return

        # Get item from sequence only once, for speed
        k_val = seq[k]

        # Working backwards starting with the last item,           k     i
        # find the first one greater than the one at k       0 0 1 0 1 1 1 0
        for i in i_indices:
            if k_val < seq[i]:
                break

        # Swap them in the most efficient way
        (seq[k], seq[i]) = (seq[i], seq[k])                #       k     i
                                                           # 0 0 1 1 1 1 0 0

        # Reverse the part after but not                           k
        # including k, also efficiently.                     0 0 1 1 0 0 1 1
        seq[k + 1:] = seq[-1:k:-1]

# end of code from stackoverflow


def generate_movement_sequences():
#    positive_sequences = itertools.product(positive_directions, repeat=max_steps//2) # this would generate duplicates later on through permutations
    positive_sequences = itertools.combinations_with_replacement(positive_directions, max_steps//2)
    
    positive_and_negative = []    
    for sequence in positive_sequences:
#        positive_and_negative.append((itertools.chain.from_iterable((x, x*-1) for x in sequence))) # this works for np.array like vectors as up/down
        positive_and_negative.append(sequence + tuple([tuple([y*-1 for y in direction]) for direction in sequence]))

    movement_sequences = []        
    for sequence in positive_and_negative:
#        movement_sequences.append((itertools.permutations(sequence)))    # this would not generate unique permutations  
        # generate unique permutations. here would be a good points to unify them, not later, because in each set there can be (=there are) some of them
        movement_sequences.append(unique_permutations(sequence))
    
    return movement_sequences
        

def iterate(ants):
    # due to massive performance drop, X, Y is only generated once. No cleanup necessary        
    Y, X = np.mgrid[-1:-dim_y:dim_y*1j, 1:dim_x:dim_x*1j]    
    # generate all possible sequences of movement
    movement_sequences = generate_movement_sequences()
    print("time to setup sequence generators: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))
    
    i = 0
    for subsequences in movement_sequences:
        for movement_sequence in subsequences:
            i += 1

            U, V = init_meshgrids()            
            field = ants.copy()  
            
            if iterate_over_each(X, Y, U, V, movement_sequence, field):                   
                if legal_sequence(U, V, field):
                    if plot_fields:
                        plot(X, Y, U, V)
                        print("sequence id: ", '{:,}'.format(i).replace(',', ' '), "| total solutions so far:", len(valid_sequences)+1)
                    valid_sequences.append(i)
               
            if i % 500000 == 0:
                global block_time
                print("elapsed time per block: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - block_time))
                block_time = time.time()
                print("current sequencing id: ", '{:,}'.format(i).replace(',', ' '))
    
                
    print("found solutions: ", len(valid_sequences), "| out of sequences:", i)     
    print("sequence IDs of solutions")
    if plot_fields:
        plot_array(valid_sequences)
        
plot_fields = False
plot_fields = True
profile_run = False

if profile_run == False:
    iterate(ants)
else:
    import profile 
    profile.run('iterate(ants)')   

print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))