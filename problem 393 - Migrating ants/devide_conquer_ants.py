# -*- coding: utf-8 -*-
"""
10 x 10 result 112398351350823112
runtime: 99.39s
"""
from pprint import pprint
import sys
import time
start_time = time.time() 

"""
devide field in small blocks
use block size 1x1
each block has 4 edges
each edge has influx and outflux requirements
e.g. 1x1 block with moving ant upwards has:
    * top edge: outflux, no influx (influx would result in swap)
    * bot, left, right has influx, but only one, so lets split up the block
    
define 3 kind of blocks: * outflux up, 
                         * no influx on up, left, bot
                         * influx on right
                         
                         * outflux up,
                         * no influx on up, left, right
                         * influx on bot
                         
                         * [third kind]
                         
then rotate this construct by 90, 180 and 270 to create in sum 4 states                        

so we have now 4*3 = 12 different kind of monoblocks (1x1)
                         
let's not care about the internal states of the blocks, just care about borders
so record number of variants for each state defined by borders
on 1x1 block, there is always only 1 variant, this will increase later on

now we create all different kind of 1x2 blocks, record border states and number
of possibilities to create this states (should be still 1 per block)

then create 2x2 block out of 1x2 blocks

it is known by meshgrid_ants:
    
    2x2: 2
    2x4: 6
    4x4:88 (after 1000s)
    
by this script    
    8x4 : 39844
    8x8 : 22902801416 (2s)
    10x10: 112398351350823112 (100s)
    
    ARROW_UP = '\u2191'   
    ARROW_RIGHT = '\u2190' 
    ARROW_DOWN = '\u2193'
    ARROW_LEFT = '\u2192'
    LUT = [ARROW_UP, ARROW_RIGHT, ARROW_DOWN, ARROW_LEFT]    
"""
from collections import Counter, namedtuple

# a Bluck is the datatype of a Block. Its immutable and hashable to be usefull in Counter
Bluck = namedtuple("Bluck", ["influx", "outflux", "size"])

def generate_upright_1x1_seed_block():
    return Bluck(size=(1,1), outflux=(tuple([1]),tuple([0]),tuple([0]),tuple([0])), influx=(tuple([0]),tuple([1]),tuple([0]),tuple([0]))) # edges are indexed by up, right, bot, left = 0,1,2,3

    
def rotate_by_one(flux):
    return (flux[3], flux[0], flux[1], flux[2])
   
        
    # take upright outflux with the 3 possible influxes (upright inflix would be a swap, hence only 3 blocks)
def generate_all_upright_1x1_blocks():
    block = generate_upright_1x1_seed_block()    
    blocks = Counter([block]) #original block
    for i in range(2):  
        block_rotated = Bluck(rotate_by_one(block.influx), block.outflux, block.size)
        blocks.update([block_rotated])   
        block = block_rotated     
    return blocks


def generate_all_1x1_blocks():    
    blocks = generate_all_upright_1x1_blocks()
    all_blocks = Counter()
    for block in blocks:
        all_blocks.update([block]) # original block    
        for i in range(3):  
            block_rotated = Bluck(rotate_by_one(block.influx), rotate_by_one(block.outflux), block.size)
            all_blocks.update([block_rotated])   
            block = block_rotated  
    return all_blocks

       
    # stack_vertical: stack horizontal or vertical. border: side with no out/influx allowed
    # this function is called for a 8x4=32 grid 500.000x, takes 1.1s before optimization
def stack_2_blocks(upper_block, lower_block, stack_vertical, border):        
    if stack_vertical == False:       
        touching_sides = {"upper":1, "lower":3} # "upper" is the block on the right side in horizontal stack_vertical
    else:
        touching_sides = {"upper":2, "lower":0} 

    # check if upper matches to lower (this automatically ensures not being a swap, since influx can never be on an outflux site since no such seed block)  
    if \
        (upper_block.outflux[touching_sides["upper"]] == lower_block.influx[touching_sides["lower"]][::-1]) and\
        (lower_block.outflux[touching_sides["lower"]] == upper_block.influx[touching_sides["upper"]][::-1]):

        # check if border violation, blocks that have flux over border are not needed 
        # having this check before matching check increases calculation time by 3x
        for side in (border-set([touching_sides["upper"]])):
            for direction in ["outflux", "influx"]: 
                if 1 in getattr(upper_block, direction)[side]:
                    return False, None
                    
        for side in (border-set([touching_sides["lower"]])):
            for direction in ["outflux", "influx"]: 
                if 1 in getattr(lower_block, direction)[side]:
                    return False, None    
         
        # generate new block in old style dictionary. this might be a faster, if directly fed into a bluck
        block = dict()
        # edges are indexed by up, right, bot, left = 0,1,2,3 (inside an edge numbering follows clockwise)
        # flow on touching edges is consumed/not reported anymore/does not matter   
        
        if stack_vertical == True:
            block["size"] = (upper_block.size[0],\
                             upper_block.size[1]+lower_block.size[1])
            # edges are indexed by up, right, bot, left = 0,1,2,3 (inside an edge numbering follows clockwise)
            # flow on touching edges is consumed/not reported anymore/does not matter
            for direction in ["outflux", "influx"]:
                block[direction] = (getattr(upper_block, direction)[0],\
                                    getattr(upper_block, direction)[1]+getattr(lower_block, direction)[1],\
                                    getattr(lower_block, direction)[2],\
                                    getattr(lower_block, direction)[3]+getattr(upper_block, direction)[3])  
        else:
            block["size"] = (upper_block.size[0]+lower_block.size[0],\
                             upper_block.size[1])
            for direction in ["outflux", "influx"]:
                block[direction] = (getattr(upper_block, direction)[0]+getattr(lower_block, direction)[0],\
                                    getattr(lower_block, direction)[1],\
                                    getattr(lower_block, direction)[2]+getattr(upper_block, direction)[2],\
                                    getattr(upper_block, direction)[3])            
        return True, Bluck(**block)
    else:
        return False, None  

        
def generate_all_combinations(upper_blocks, lower_blocks, stack_vertical, border):
    output_blocks = Counter()
    for upper_block,u in upper_blocks.items():
        for lower_block,l in lower_blocks.items():
            fit_together, stacked_block = stack_2_blocks(upper_block, lower_block, stack_vertical, border)
            if fit_together == True:
                output_blocks.update({stacked_block: u*l})    
    return output_blocks  

           
# investigate required buildings blocks    
def build_up_grid(x=10, y=10, border=set([0,1,2,3])):
    slice_vertical = (x >= y) # slice always through longer side    
    if not (x==1 and y==1):
        if slice_vertical==True:            
            upper_block = build_up_grid(x//2, y, border-set([2]))
            lower_block = build_up_grid(x-x//2, y, border-set([0]))                
        else:
            upper_block = build_up_grid(x, y//2, border-set([1]))
            lower_block = build_up_grid(x, y-y//2, border-set([3]))  
        
        grid = generate_all_combinations(upper_block, lower_block, slice_vertical, border)    
        return grid
    else:
        return generate_all_1x1_blocks()

            
def test_known_config(x,y,expected=0):
    n = devide_and_conquer(x,y)
    if expected == 0:
        print(x, "x", y, "result", n)            
        return False
    if n != expected:
        print(x, "x", y, "test failed with", n)
        return False
    else:
        print(x, "x", y, "test passed with", n)
        return True

        
def test_algorithm_recursive():
    if test_known_config(2,2,2):
        if test_known_config(2,4,6):    
            if test_known_config(4,4,88):
                if test_known_config(8,8,22902801416): # expected value not confirmed by meshgrid - 2s runtime           
                    test_known_config(10,10,112398351350823112) # after 100s

                    
# gives end result: number of combinations    
def count_combinations(blocks):
    counter = 0
    for _, n in blocks.items():
        counter += n
    return counter

    
# if you want to generate something, call this
def devide_and_conquer(x,y):        
    blocks = build_up_grid(x,y)
    grid_combinations = count_combinations(blocks) # calculate end result
    print("for a", x, "x", y, "grid there are", grid_combinations, "possibilites")
    return grid_combinations
        

def solve_problem():
    test_algorithm_recursive()

    
solve_problem() 
#import profile 
#profile.run('test_known_config(10,10,112398351350823112)') 
print("runtime: \x1b[1;31m%.2fs\x1b[0m" % (time.time() - start_time))