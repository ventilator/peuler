# -*- coding: utf-8 -*-
"""

"""
import copy
from pprint import pprint
import sys
import time
import numpy as np
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
    8x4 : 39844 (not confirmed by meshgrid)    
    
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
    return Bluck(size=(1,1), outflux=(tuple([1]),tuple([0]),tuple([0]),tuple([0])), influx=(tuple([1]),tuple([0]),tuple([0]),tuple([0]))) # edges are indexed by up, right, bot, left = 0,1,2,3

    
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
            
        # generate new block
        block = dict()
        # edges are indexed by up, right, bot, left = 0,1,2,3 (inside an edge numbering follows clockwise)
        # flow on touching edges is consumed/not reported anymore/does not matter   
        #  block["size"] = [x,y]
        # generate new block
        
        if stack_vertical == True:
            block["size"] = (upper_block.size[0], upper_block.size[1]+lower_block.size[1])
            if upper_block.size[0] != lower_block.size[0]:
                sys.exit("Warning: blocks cannot be stacked, size missmatch")
                return False, None
            # edges are indexed by up, right, bot, left = 0,1,2,3 (inside an edge numbering follows clockwise)
            # flow on touching edges is consumed/not reported anymore/does not matter
            for direction in ["outflux", "influx"]:
                block[direction] = (getattr(upper_block, direction)[0], getattr(upper_block, direction)[1]+getattr(lower_block, direction)[1], getattr(lower_block, direction)[2], getattr(lower_block, direction)[3]+getattr(upper_block, direction)[3])  
        else:
            block["size"] = (upper_block.size[0]+lower_block.size[0], upper_block.size[1])
            if upper_block.size[1] != lower_block.size[1]:
                print("Warning: blocks cannot be stacked, size missmatch")
                return False, None
            for direction in ["outflux", "influx"]:
                block[direction] = (getattr(upper_block, direction)[0]+getattr(lower_block, direction)[0], getattr(lower_block, direction)[1], getattr(lower_block, direction)[2]+getattr(upper_block, direction)[2], getattr(upper_block, direction)[3])            
          
        return True, Bluck(**block)
    else:
        return False, None  

def generate_all_combinations(upper_blocks, lower_blocks, stack_vertical, border):
    output_blocks = Counter()
    for upper_block in upper_blocks:
        for lower_block in lower_blocks:
            fit_together, stacked_block = stack_2_blocks(upper_block, lower_block, stack_vertical, border)
            if fit_together == True:
                output_blocks.update([stacked_block])
    return output_blocks  

    
stacks_logger = []             
# investigate required buildings blocks    
def build_up_grid(x=10, y=10, border=set([0,1,2,3])):
    global stacks_logger
    stacks_logger.append([x,y,border])
    #print("stackings so far:",len(stacks), "recently", [x,y,slice_vertical,border])
    
    slice_vertical = (x >= y) # slice always through longer side (+ this is a fix for irregular sizes e.g. 10x10)
    
    if x == 0 or y == 0:
        sys.exit("attempt to generate a 0xn grid")
    else:
        if not (x==1 and y==1):
            if slice_vertical==True:            
                upper_block = build_up_grid(x//2, y, border-set([2]))
                lower_block = build_up_grid(x-x//2, y, border-set([0]))                
            else:
                upper_block = build_up_grid(x, y//2, border-set([1]))
                lower_block = build_up_grid(x, y-y//2, border-set([3]))  
            
            ul = len(upper_block) 
            ll = len(lower_block)
            print("stackings:",len(stacks_logger), "zZ", x, "x", y, "out of", ul, "x", ll, "combinations:", ll*ul)    
            grid = generate_all_combinations(upper_block, lower_block, slice_vertical, border)    
            print("sucessfull stackings:", round(len(grid)/(ll*ul),3), "grids:", len(grid))
#            if x==4 and y==4:
#                count_unique_stacks(grid)
            return grid
        else:
            global counter
            counter += 1
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
                if test_known_config(8,8,22902801416): # expected value not confirmed by meshgrid - sum runtime = 8.8s, now under 6s
                    return 0              
                    test_known_config(10,10)

demo_generator = False


# 8x4: stackings: 63 unique: 31: potential speed boost through chaching: 2x    
# 8x8: stackings: 127 unique: 40: speed boost: 3x
# 10x10: stackings: 199 unique: 71 :speed boost: 3x   


"""
    fix list: 
        slicer for 10x10 -done
        evaluate caching speed boost for 10x10 -done: 3x: evaluation: not worth the effort right now
        evaluate ram problem for 8x8 --e.g. a 4x4 with two bordes can be created in 10152 but only 523 unique interfaces --> this can be 20x reduced
        next step: get 8x8 going --> implemented, success after 8 seconds
        10x10 still out of reach, 3x5 stacking is a large brocken (2.2M combinations)
"""

# gives end result: number of combinations    
def count_combinations(blocks):
    counter = 0
    for _, n in blocks.items():
        counter += n
    return counter

    
# only call this if you want to generate something
def devide_and_conquer(x,y):        
    global counter
    counter = 0     
    global stacks_logger
    stacks_logger = []
    blocks = build_up_grid(x,y)
    pprint(blocks)
    grid_combinations = count_combinations(blocks) # calculate end result
    print("for a", x, "x", y, "grid there are", grid_combinations, "possibilites")
    
    if not x*y == counter: # failure check
        print("generation failure for", x, "x", y, ".")
        print("unit cells:", counter, "expected", x*y)    
        
    return grid_combinations
        

def solve_problem():
#    test_algorithm_manually()
    test_algorithm_recursive()

#    devide_and_conquer(4,4)
    
#build_up()
#from pympler import asizeof
solve_problem()  
#
#import profile 
#profile.run('solve_problem()') 

print("runtime: \x1b[1;31m%.2fs\x1b[0m" % (time.time() - start_time))
#print("memory: \x1b[1;31m%.2fM\x1b[0m" % (asizeof.asizeof(grid)/1000/1000))



# ------------------old testing funcitons----------------------------------------------
def build_up_closed_4x4():
    seed_1x1_blocks = generate_all_1x1_blocks()
    blocks_1x2 = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, True, [])  
    blocks_2x2_dl = generate_all_combinations(blocks_1x2, blocks_1x2, False, [2,3]) 
    blocks_2x2_dr = generate_all_combinations(blocks_1x2, blocks_1x2, False, [1,2]) 
    blocks_2x2_ul = generate_all_combinations(blocks_1x2, blocks_1x2, False, [0,3]) 
    blocks_2x2_ur = generate_all_combinations(blocks_1x2, blocks_1x2, False, [0,1])

    blocks_2x4_l = generate_all_combinations(blocks_2x2_ul, blocks_2x2_dl, True, [0,2,3])   
    blocks_2x4_r = generate_all_combinations(blocks_2x2_ur, blocks_2x2_dr, True, [0,1,2]) 

    blocks_4x4 = generate_all_combinations(blocks_2x4_l, blocks_2x4_r, False, [0,1,2,3])       

    return len(blocks_4x4)
    
    
def build_up_closed_2x4():
    seed_1x1_blocks = generate_all_1x1_blocks()
    blocks_1x2 = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, True, [])  
    blocks_2x2_u = generate_all_combinations(blocks_1x2, blocks_1x2, False, [0,1,3]) 
    blocks_2x2_l = generate_all_combinations(blocks_1x2, blocks_1x2, False, [1,2,3])
    blocks_2x4 = generate_all_combinations(blocks_2x2_u, blocks_2x2_l, True, [0,1,2,3]) 
    return len(blocks_2x4)    
    
    
def build_up_closed_2x2():
    seed_1x1_blocks = generate_all_1x1_blocks()
    blocks_1x2_l = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, True, [0,2,3]) 
    blocks_1x2_r = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, True, [0,1,2])       
    blocks_2x2 = generate_all_combinations(blocks_1x2_l, blocks_1x2_r, False, [0,1,2,3]) 
    return len(blocks_2x2)    
 
    
def test_algorithm_manually():
    seed_1x1_blocks = generate_all_1x1_blocks()
    if len(seed_1x1_blocks) != 12:
        print("Warning:", len(seed_1x1_blocks), "1x1 have been generated. Should be 12")   
    
    n_2x2 = build_up_closed_2x2()
    if n_2x2 != 2:
        print("2x2 test failed with", n_2x2)
    else:
        print("2x2 test passed with", n_2x2)
        
    n_2x4 = build_up_closed_2x4()
    if n_2x4 != 6:
        print("2x4 test failed with", n_2x4)
    else:
        print("2x4 test passed with", n_2x4)            
        
    n_4x4 = build_up_closed_4x4()
    if n_4x4 != 88:
        print("4x4 test failed with", n_4x4)
    else:
        print("4x4 test passed with", n_4x4)   