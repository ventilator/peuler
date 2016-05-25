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

# with caching of the previous sequence: 88 solutions in 1060s (with drawing)
# found solutions:  88 | out of sequences: 163963800
# next step: due to symmetrie resions this can be cut in half

import numpy as np
import itertools
import operator
import sys

# for plotting
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import lexicographic_permutation

import time
start_time = time.time()  
block_time = start_time  

dim_x = 4
dim_y = 4
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
#up = 1
#right = 10
directions = [up, down, left, right]
positive_directions = [up, right]
negative_directions = [down, left]

start_point = np.array([0,0])
total_steps = 0
valid_sequences = []
ants = np.zeros([dim_y, dim_x])

plot_fields = False
#plot_fields = True
plot_statistics = True
plot_statistics = False

test_some_iterations = True
test_some_iterations = False
printout_cache = True
printout_cache = False

activate_cache = True
#activate_cache = False
times_cache_used = 0

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
    
def plot_scatter(array2D):
    x = []
    y = []
    for x_,y_ in array2D:
        x.append(x_)
        y.append(y_)
        
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


caching_field = []
caching_U = []
caching_V = []
caching_movement_sequence = []

def cache(field, U, V, sequence, step):
    caching_field[step] = field.copy()
    caching_U[step] = U.copy()
    caching_V[step] = V.copy()
    caching_movement_sequence[step] = sequence
    # invalidate future steps from last iteration # needs only be done if cache is accessed
#    for i in range(step+1, max_steps):
#        caching_movement_sequence[i] = None
    global times_cache_used
    times_cache_used += 1

def init_cache(size):
    global caching_field
    global caching_U
    global caching_V
    global caching_movement_sequence
    caching_field = [None] * size
    caching_U = [None] * size
    caching_V = [None] * size
    caching_movement_sequence = [None] * size

def get_cache_and_delete_future(step):
    # invalidate future steps from last iteration
    global caching_movement_sequence
    for i in range(step+1, max_steps):
        caching_movement_sequence[i] = None

    global caching_field
    global caching_U
    global caching_V
    
    return caching_field[step].copy(), caching_U[step].copy(), caching_V[step].copy()     
   
def print_cache():
    if printout_cache == True:
        print("cached sequence")
        print(caching_movement_sequence)
        print("cached field")
        for y in caching_field:
            print(y)    
    

def iterate_over_each(U, V, movement_sequence, field):
    def check_boundary(x,y):
        return (0 <= y < dim_y) and (0 <= x < dim_x)
    
    step = 0
    using_cached_values = True
    print_cache()
    # iterate over each koordinate and apply a particular movement sequence
    for y in range(dim_y): #hardcoded dim_? instead of len(), because faster        
        for x in range(dim_x):
            iterate = True
            if activate_cache == True:
                if (using_cached_values==True):
                    if (movement_sequence[step] == caching_movement_sequence[step]):
    #                    print("doing nothing since there is a cached value present", movement_sequence[step])
                        iterate = False
                    else:
                        #if we drop out because of missmatch
#                        print("no cached sequence found, walking into new territory", movement_sequence[step])
                        # resetting state with cached values
                        using_cached_values=False
                        if (step != 0):
                            field, U, V = get_cache_and_delete_future(step-1)
                
                
            if (activate_cache == False) or (iterate == True): 
                if printout_cache == True:
                    print("processing", movement_sequence[step])
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
                        return False, field, U, V
                        
                    field[y_v, x_u] += 1 # ant comes here  
    #                if field[y-v, x+u] > 2: # more ants are already here than will walk away
    #                    return False                                                      
    
                else:
                    # walking out of grid
                    return False, field, U, V
                    
                U[y, x] = u 
                V[y, x] = v                  
                
                if activate_cache == True:
                    cache(field, U, V, movement_sequence[step], step)
                    print_cache()
                
            step += 1

    return True, field, U, V


def generate_movement_sequences():
#    positive_sequences = itertools.product(positive_directions, repeat=max_steps//2) # this would generate duplicates later on through permutations
    positive_sequences = itertools.combinations_with_replacement(positive_directions, max_steps//2)
    
    positive_and_negative = []    
    for i,sequence in enumerate(positive_sequences): 
        # print(i)
        #let at least some ups/down and lefts/rights be there in order to enable at least two rotations in 2D subsequence (no need for only ups or only rights)
        if (i >= dim_x//2) and (i <= (dim_y*dim_x)//2-dim_y//2):
            
            print("positive seeds", sequence)
    #        positive_and_negative.append((itertools.chain.from_iterable((x, x*-1) for x in sequence))) # this works for np.array like vectors as up/down
            positive_and_negative.append(sequence + tuple([tuple([y*-1 for y in direction]) for direction in sequence]))
    #        positive_and_negative.append(sequence + tuple([direction*-1 for direction in sequence]))
            
    movement_sequences = []        
    for i, sequence in enumerate(positive_and_negative):
#        print("positive with negative counters", sequence)
#        movement_sequences.append((itertools.permutations(sequence)))    # this would not generate unique permutations  
        # generate unique permutations. here would be a good points to unify them, not later, because in each set there can be (=there are) some of them
#        movement_sequences.append(unique_permutations(sequence)) 
#        if i == 2:
        movement_sequences.append(lexicographic_permutation.next_permutation(list(sequence))) 
#            movement_sequences.append(unique_permutations(sequence)) 
        
    return movement_sequences


def testit():
    sequs = generate_movement_sequences()
    lst = []
    for x in sequs:
        print("new sequence:")
        for y in x:
            print(y)
            lst.append(y)
#    lst.sort()
#    for item in lst:
#        print(item)
        
#testit()
#sys.exit()

def iterate(ants):
    # due to massive performance drop, X, Y is only generated once. No cleanup necessary        
    Y, X = np.mgrid[-1:-dim_y:dim_y*1j, 1:dim_x:dim_x*1j]    
    # generate all possible sequences of movement
    movement_sequences = generate_movement_sequences()
    print("time to setup sequence generators: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))
    
    i = 0
    valid_sequences_per_seed = []
    init_cache(max_steps)
    for seed,subsequences in enumerate(movement_sequences):
#        print("looking at next seed.", seed,"think about excluding a seed if it has no solution")
        valid_sequences_in_this_seed = 0
        for movement_sequence in subsequences:
            i += 1
            if test_some_iterations == True:                  
                print(movement_sequence, "(current sequence)")
            U, V = init_meshgrids()            
            field = ants.copy()  
            
            no_objection, field, U, V = iterate_over_each(U, V, movement_sequence, field)
            if no_objection == True:                   
                if legal_sequence(U, V, field):
                    if plot_fields:
                        plot(X, Y, U, V)
                        print("sequence id: ", '{:,}'.format(i).replace(',', ' '), "| total solutions so far:", len(valid_sequences)+1)
                    valid_sequences.append(i)
                    valid_sequences_in_this_seed += 1
               
            if i % 500000 == 0:
                global block_time
                print("elapsed time per block: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - block_time))
                block_time = time.time()
                print("current sequencing id: ", '{:,}'.format(i).replace(',', ' '))
             
#            if i == 664:
#                print("######## processing iteration id", i+1)
#                global test_some_iterations
#                global printout_cache
#                
#                test_some_iterations = True
#                printout_cache = True
#                
#            if i == 665:
#                print("we are at step", i)
#                print("this should be valid")
#                print(U, "U")
#                print(V, "V")
#                print("caching U")
#                for Uu in caching_U:
#                    print(Uu)
#                
#                plot(X, Y, U, V)
#                print("######## processing iteration id", i+1)
#                
#            if i == 666:
#                print("######## processing iteration id", i+1)
#                sys.exit()  
                
            if test_some_iterations == True:
#                if i == 3:
                if times_cache_used > 100:
                    sys.exit()
#        print("found solutions in this seed", valid_sequences_in_this_seed)  
        valid_sequences_per_seed.append([seed, valid_sequences_in_this_seed])
        
    print("found solutions: ", len(valid_sequences), "| out of sequences:", i)     
    if plot_statistics:
        print("sequence IDs of solutions")
        plot_array(valid_sequences)
        print("legal sequences per seed of vectors")
        plot_scatter(valid_sequences_per_seed)
        




profile_run = True
profile_run = False
if profile_run == False:
    iterate(ants)
else:
    import profile 
    profile.run('iterate(ants)')   

print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))