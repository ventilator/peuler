# -*- coding: utf-8 -*-
"""

"""
import copy
import pprint
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
"""


def generate_upright_1x1_seed_block():
    block = dict()
    block["size"] = [1,1]
    # edges are indexed by up, right, bot, left = 0,1,2,3
    block["outflux"] = [[1],[0],[0],[0]]
    block["influx"] = [[0],[1],[0],[0]]
    return block
    
    
def rotate_by_one(array):
    last = array.pop()
    array.insert(0, last)
    return array

    
def get_arrow(edge_array):
    ARROW_UP = '\u2191'   
    ARROW_RIGHT = '\u2190' 
    ARROW_DOWN = '\u2193'
    ARROW_LEFT = '\u2192'
    LUT = [ARROW_UP, ARROW_RIGHT, ARROW_DOWN, ARROW_LEFT]
    for i, edge in enumerate(edge_array):
        if edge == [1]:
            return LUT[i]
    return "no flux found"    

    
def block_printer(block):
#    print(block["outflux"], "outflux")                
#    print(block["influx"], "influx")                
    print(get_arrow(block["outflux"]), "outflux")
    print(get_arrow(block["influx"]), "influx")


# pretty sure this block printer does not print left/right side with possible 2 arrows    
def _1x2_block_printer(upper, lower):
    print("o", get_arrow(upper["outflux"]), "i", get_arrow(upper["influx"]))
    print("i", get_arrow(lower["influx"]), "o", get_arrow(lower["outflux"]))
    print("_")
    
        
    # take upright outflux with the 3 possible influxes (upright inflix would be a swap, hence only 3 blocks)
def generate_all_upright_1x1_blocks():
    block = generate_upright_1x1_seed_block()    
    blocks = []
    blocks.append(copy.deepcopy(block)) # original block    
    for i in range(2):  
        block["influx"] = rotate_by_one(block["influx"])
        blocks.append(copy.deepcopy(block)) # two additional shifted blocks    
    return blocks


def generate_all_1x1_blocks():    
    blocks = generate_all_upright_1x1_blocks()
    all_blocks = []
    for block in blocks:
        all_blocks.append(copy.deepcopy(block)) # original block    
        for i in range(3):  
            block["influx"] = rotate_by_one(block["influx"])
            block["outflux"] = rotate_by_one(block["outflux"])
            all_blocks.append(copy.deepcopy(block)) # three additional rotated blocks of blocks           
    return all_blocks
    

def integrity_check(block):
    passing = True
    if sum(sum(x) for x in block["outflux"]) != sum(sum(x) for x in block["influx"]):    
        passing = False
        
    if not passing:        
        pprint.pprint(block)     
        sys.exit("invalid block")        
    return passing    


def plot(block):
    pass

        
    #configuration: stack horizontal or vertical. border: side with no out/influx allowed
def stack_2_blocks(upper_block, lower_block, configuration, border):
    #check 
#    integrity_check(upper_block)
#    integrity_check(lower_block)
#    if upper_block["size"] == [1,2] and upper_block["outflux"] == [[1], [0, 0], [0], [0, 0]] and upper_block["influx"] == [[0], [0, 1], [0], [0, 0]]:
##        pprint.pprint(upper_block)
#        if lower_block["size"] == [1,2] and lower_block["outflux"] == [[0], [0, 0], [0], [1, 0]] and lower_block["influx"] == [[1], [0, 0], [0], [0, 0]]:
#            print("this should match")
#            pprint.pprint(lower_block)
        
    fit_together = False
    if configuration == "horizontal":
        # "upper" is the block on the right side in horizontal configuration
        touching_sides = {"upper":1, "lower":3} 
    else:
        if configuration == "vertical":
            touching_sides = {"upper":2, "lower":0} 
        else:
            print("illegal stacking configuration")
            return False, None
            
    # check if upper matches to lower (this automatically ensures not being a swap, since influx can never be on an outflux site since no such seed block)
    
    if \
        (upper_block["outflux"][touching_sides["upper"]] == lower_block["influx"][touching_sides["lower"]][::-1]) and\
        (lower_block["outflux"][touching_sides["lower"]] == upper_block["influx"][touching_sides["upper"]][::-1]):
        #(sum(upper_block["outflux"][touching_sides["upper"]] + lower_block["outflux"][touching_sides["lower"]]) < len(upper_block["outflux"][touching_sides["upper"]])+1):
        fit_together = True
        
        # generate new block
        block = dict()
        
        if configuration == "vertical":
                            #x,y
            block["size"] = [upper_block["size"][0], upper_block["size"][1]+lower_block["size"][1]]
            if upper_block["size"][0] != lower_block["size"][0]:
                sys.exit("Warning: blocks cannot be stacked, size missmatch")
                return False, None
            # edges are indexed by up, right, bot, left = 0,1,2,3 (inside an edge numbering follows clockwise)
            # flow on touching edges is consumed/not reported anymore/does not matter
            for direction in ["outflux", "influx"]:
                block[direction] = [upper_block[direction][0], upper_block[direction][1]+lower_block[direction][1], lower_block[direction][2], lower_block[direction][3]+upper_block[direction][3]]  
        else:
            block["size"] = [upper_block["size"][0]+lower_block["size"][0], upper_block["size"][1]]
            if upper_block["size"][1] != lower_block["size"][1]:
                print("Warning: blocks cannot be stacked, size missmatch")
                return False, None
            for direction in ["outflux", "influx"]:
                block[direction] = [upper_block[direction][0]+lower_block[direction][0], lower_block[direction][1], lower_block[direction][2]+upper_block[direction][2], upper_block[direction][3]]            
        
        # check if border violation 
        for side in border:
            for direction in ["outflux", "influx"]: 
                if sum(block[direction][side]) != 0:
                    return False, None
                
        return fit_together, block
    else:
        fit_together = False
    return fit_together, None     
        
         
def generate_all_combinations(upper_blocks, lower_blocks, configuration, border):
    if upper_blocks == None or lower_blocks == None or len(upper_blocks) == 0 or len(lower_blocks) == 0:
        pprint.pprint(upper_blocks)
        pprint.pprint(lower_blocks)
        sys.exit("failure, no input_blocks")
    output_blocks = []
    for upper_block in upper_blocks:
        for lower_block in lower_blocks:
            fit_together, stacked_block = stack_2_blocks(upper_block, lower_block, configuration, border)
            if fit_together == True:
                output_blocks.append(stacked_block)
#    if len(output_blocks) > 0:            
#        print("generated", len(output_blocks), output_blocks[0]["size"], "out of", len(upper_blocks), upper_blocks[0]["size"], "and",  len(lower_blocks), lower_blocks[0]["size"] )            
    return output_blocks      
      

def build_up_closed_4x4():
    seed_1x1_blocks = generate_all_1x1_blocks()
    blocks_1x2 = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, "vertical", [])  
    blocks_2x2_dl = generate_all_combinations(blocks_1x2, blocks_1x2, "horizontal", [2,3]) 
    blocks_2x2_dr = generate_all_combinations(blocks_1x2, blocks_1x2, "horizontal", [1,2]) 
    blocks_2x2_ul = generate_all_combinations(blocks_1x2, blocks_1x2, "horizontal", [0,3]) 
    blocks_2x2_ur = generate_all_combinations(blocks_1x2, blocks_1x2, "horizontal", [0,1])

    blocks_2x4_l = generate_all_combinations(blocks_2x2_ul, blocks_2x2_dl, "vertical", [0,2,3])   
    blocks_2x4_r = generate_all_combinations(blocks_2x2_ur, blocks_2x2_dr, "vertical", [0,1,2]) 

    blocks_4x4 = generate_all_combinations(blocks_2x4_l, blocks_2x4_r, "horizontal", [0,1,2,3])       

    return len(blocks_4x4)
    
    
def build_up_closed_2x4():
    seed_1x1_blocks = generate_all_1x1_blocks()
    blocks_1x2 = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, "vertical", [])  
    blocks_2x2_u = generate_all_combinations(blocks_1x2, blocks_1x2, "horizontal", [0,1,3]) 
    blocks_2x2_l = generate_all_combinations(blocks_1x2, blocks_1x2, "horizontal", [1,2,3])
    blocks_2x4 = generate_all_combinations(blocks_2x2_u, blocks_2x2_l, "vertical", [0,1,2,3]) 
    return len(blocks_2x4)    
    
    
def build_up_closed_2x2():
    seed_1x1_blocks = generate_all_1x1_blocks()
    blocks_1x2_l = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, "vertical", [0,2,3]) 
    blocks_1x2_r = generate_all_combinations(seed_1x1_blocks, seed_1x1_blocks, "vertical", [0,1,2])       
    blocks_2x2 = generate_all_combinations(blocks_1x2_l, blocks_1x2_r, "horizontal", [0,1,2,3]) 
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
        
        
def test_known_config(x,y,expected=0):
    grid = devide_and_conquer(x,y)
    n = len(grid)
    if expected == 0:
        print(x, "x", y, "result", n)            
        return grid
    if n != expected:
        print(x, "x", y, "test failed with", n)
    else:
        print(x, "x", y, "test passed with", n)
    return grid        

        
def test_algorithm_recursive():
    test_known_config(2,2,2)
    test_known_config(4,2,6)    
    test_known_config(4,4,88)      
    test_known_config(6,4)  
    test_known_config(8,4)      
    test_known_config(8,6) # more than 1GB RAM...
    
def test_memory():
#    from pympler import asizeof
    grid = test_known_config(8,4,88)  
    
#    print(asizeof.asizeof(grid))
        

def devide_and_conquer(x,y):        
    global counter
    counter = 0        
    grid = build_up_grid(x,y) 
    if not x*y == counter :
        print("generation failure for", x, "x", y, ".")
        print("unit cells:", counter, "expected", x*y) 
    grid_combinations = len(grid)
    print("for a", x, "x", y, "grid there are", grid_combinations, "possibilites")
    return grid

    
# deletes an item from a list, returning not None if item is not in list but list itself
def list_delete(alist, item):
    if item in alist:
        blist = alist[:]
        blist.remove(item)
        return blist
    else:
        return alist.copy()

            
# investigate required buildings blocks    
def build_up_grid(x=10, y=10, polarization="vertical", border=[0,1,2,3]):
#    print(x, "x", y, polarization, border)
    if x == 0 or y == 0:
        sys.exit("attempt to generate a 0xn grid")
    else:
        if not (x==1 and y==1):
            if polarization=="vertical":            
                upper_block = build_up_grid(x//2, y, "horizontal", list_delete(border, 2))
                lower_block = build_up_grid(x-x//2, y, "horizontal", list_delete(border, 0))                
            else:
                upper_block = build_up_grid(x, y//2, "vertical", list_delete(border, 1))
                lower_block = build_up_grid(x, y-y//2, "vertical", list_delete(border, 3))  
                
            return generate_all_combinations(upper_block, lower_block, polarization, border)    
        else:
            global counter
            counter += 1
            return generate_all_1x1_blocks()
            
            
            

def solve_problem():
#    test_algorithm_manually()
#    test_algorithm_recursive()
    test_memory()
#    devide_and_conquer(4,4)
    
#build_up()

solve_problem()  
print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))