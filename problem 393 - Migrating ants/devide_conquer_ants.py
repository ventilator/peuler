# -*- coding: utf-8 -*-
"""

"""
import copy












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
    
    
def stack_1x1_blocks(upper_block, lower_block):
    fit_together = False
    # check, if upper matches to lower and if it is not a swap
    if (upper_block["outflux"][2][0] == lower_block["influx"][0][0]) and\
        (lower_block["outflux"][0][0] == upper_block["influx"][2][0]) and\
        ((upper_block["outflux"][2][0] + lower_block["outflux"][0][0]) < 2):
        fit_together = True
        
        # generate new block
        block = dict()
                        #x,y
        block["size"] = [1,2]
        # edges are indexed by up, right, bot, left = 0,1,2,3 (inside an edge numbering follows clockwise)
        # flow on touching edges is consumed/not reported anymore/does not matter
        for direction in ["outflux", "influx"]:
            block[direction] = [upper_block[direction][0], upper_block[direction][1]+lower_block[direction][1], lower_block[direction][2], lower_block[direction][3]+upper_block[direction][3]]      
        return fit_together, block
    else:
        fit_together = False
    return fit_together, None
    
    
def generate_all_1x2_blocks():
    blocks_1x2 = []    
    blocks_1x1 = generate_all_1x1_blocks()
    print(len(blocks_1x1), "1x1 have been generated")
    for upper_block in blocks_1x1:
        for lower_block in blocks_1x1:
            fit_together, block_1x2 = stack_1x1_blocks(upper_block, lower_block)
            if fit_together == True:
                blocks_1x2.append(block_1x2)
                #_1x2_block_printer(upper_block, lower_block)    
    print(len(blocks_1x2), "blocks_1x2 fit together, out of", len(blocks_1x1)**2)
    print("demo 1x2 block", blocks_1x2[0])            


#blocks = generate_all_1x1_blocks()
#for i, block in enumerate(blocks):
##    print(i)
#    block_printer(block)    
generate_all_1x2_blocks()