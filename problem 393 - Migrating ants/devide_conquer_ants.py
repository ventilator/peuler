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
    
def block_printer(block):
    print(block["outflux"], "outflux")                
    print(block["influx"], "influx")

    
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
    
    
blocks = generate_all_1x1_blocks()
for i, block in enumerate(blocks):
    print(i)
    block_printer(block)
    
def stack_blocks(upper_block, lower_block):
    fit_together = False
    # check, if upper can or won't give something to lower and lower does not want to give something back (would be swap)
    if (upper_block["outflux"][2] == lower_block["influx"][0]) and (0 == lower_block["outflux"][0]):
        fit_together = True
    else:
        # check, if lower can or won't give something to upper and upper does not want to give something back (would be swap)
        if (lower_block["outflux"][0] == upper_block["influx"][2]) and (0 == upper_block["outflux"][2]):
            fit_together = True
    return fit_together, None
    
def generate_all_1x2_blocks():
    blocks_1x2 = []
    
    blocks_1x1 = generate_all_1x1_blocks()
    for upper_block in blocks_1x1:
        for lower_block in blocks_1x1:
            fit_together, block_1x2 = stack_blocks(upper_block, lower_block)
            if fit_together:
                blocks_1x2.append(block_1x2)
                block_printer(upper_block)
                block_printer(lower_block)                


    
generate_all_1x2_blocks()