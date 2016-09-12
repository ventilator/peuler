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
    8x4 : 39844 (not confirmed by meshgrid)
"""


def generate_upright_1x1_seed_block():
    block = dict()
    block["size"] = [1,1]
    block["uniqueness"] = 1 # this block was be generated by n ways
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

        
    #stack_vertical: stack horizontal or vertical. border: side with no out/influx allowed
def stack_2_blocks_slow(upper_block, lower_block, stack_vertical, border):
    #check 
    integrity_check(upper_block)
    integrity_check(lower_block)
        
    if stack_vertical == False:
        # "upper" is the block on the right side in horizontal stack_vertical
        touching_sides = {"upper":1, "lower":3} 
    else:
        touching_sides = {"upper":2, "lower":0} 
            
    # check if upper matches to lower (this automatically ensures not being a swap, since influx can never be on an outflux site since no such seed block)  
    if \
        (upper_block["outflux"][touching_sides["upper"]] == lower_block["influx"][touching_sides["lower"]][::-1]) and\
        (lower_block["outflux"][touching_sides["lower"]] == upper_block["influx"][touching_sides["upper"]][::-1]):

        # generate new block
        block = dict()
        
        if stack_vertical == True:
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
                
        return True, block
    else:
        return False, None     
        
       
    # stack_vertical: stack horizontal or vertical. border: side with no out/influx allowed
    # this function is called for a 8x4=32 grid 500.000x, takes 1.1s before optimization
def stack_2_blocks(upper_block, lower_block, stack_vertical, border):
        
    if stack_vertical == False:
        # "upper" is the block on the right side in horizontal stack_vertical
        touching_sides = {"upper":1, "lower":3} 
    else:
        touching_sides = {"upper":2, "lower":0} 


    # check if upper matches to lower (this automatically ensures not being a swap, since influx can never be on an outflux site since no such seed block)  
    if \
        (upper_block["outflux"][touching_sides["upper"]] == lower_block["influx"][touching_sides["lower"]][::-1]) and\
        (lower_block["outflux"][touching_sides["lower"]] == upper_block["influx"][touching_sides["upper"]][::-1]):

        # check if border violation, blocks that have flux over border are not needed 
        # having this check before matching check increases calculation time by 3x
        for side in (border-set([touching_sides["upper"]])):
            for direction in ["outflux", "influx"]: 
                if 1 in upper_block[direction][side]:
                    return False, None
                    
        for side in (border-set([touching_sides["lower"]])):
            for direction in ["outflux", "influx"]: 
                if 1 in lower_block[direction][side]:
                    return False, None                   
            
        # generate new block
        block = dict()
        block["uniqueness"] = upper_block["uniqueness"] * lower_block["uniqueness"]
        # edges are indexed by up, right, bot, left = 0,1,2,3 (inside an edge numbering follows clockwise)
        # flow on touching edges is consumed/not reported anymore/does not matter   
        #  block["size"] = [x,y]
        if stack_vertical == True:
            block["size"] = [upper_block["size"][0], upper_block["size"][1]+lower_block["size"][1]]
            for direction in ["outflux", "influx"]:
                block[direction] = [upper_block[direction][0], upper_block[direction][1]+lower_block[direction][1], lower_block[direction][2], lower_block[direction][3]+upper_block[direction][3]]  
        else:
            block["size"] = [upper_block["size"][0]+lower_block["size"][0], upper_block["size"][1]]
            for direction in ["outflux", "influx"]:
                block[direction] = [upper_block[direction][0]+lower_block[direction][0], lower_block[direction][1], lower_block[direction][2]+upper_block[direction][2], upper_block[direction][3]]            
                
        return True, block
    else:
        return False, None  


# if this block (same flux) was already created by another way, we can just keep track of number, thus reducing greatly complexity
# e.g. 4x4 grid with 2 borders consists out of 10.000 block, but only 500 unique flux configurations
import collections
def unify_stack_testing(stack):
    print("unifying...")
    counter = collections.Counter(stack)
    unified_stack = counter.keys()
    for i,count in enumerate(counter.values()):
        unified_stack[i]["uniqueness"] += count

#    for block in stack:
#        already_in_stack = False
#        for i, unified_block in enumerate(unified_stack):
#            if block["outflux"] == unified_block["outflux"] and block["influx"] == unified_block["influx"]:
#                unified_stack[i]["uniqueness"] += block["uniqueness"]
#                already_in_stack = True
#                break
#        if not already_in_stack:
#            unified_stack.append(copy.deepcopy(block))
    print("...done")
#    if len(unified_stack) != len(stack) and stack[0]['size'] == [4, 2]:
#        print("unique:")
#        pprint.pprint(unified_stack)
#        print("not unique:")
#        pprint.pprint(stack)
#        sys.exit("i did something")
    return unified_stack        

    
# if this block (same flux) was already created by another way, we can just keep track of number, thus reducing greatly complexity
# e.g. 4x4 grid with 2 borders consists out of 10.000 block, but only 500 unique flux configurations
def unify_stack(stack):
    print("unifying...")
    unified_stack = []
    for block in stack:
        already_in_stack = False
        for i, unified_block in enumerate(unified_stack):
            if block["outflux"] == unified_block["outflux"] and block["influx"] == unified_block["influx"]:
                unified_stack[i]["uniqueness"] += block["uniqueness"]
                already_in_stack = True
                break
        if not already_in_stack:
            unified_stack.append(copy.deepcopy(block))
    print("...done")
#    if len(unified_stack) != len(stack) and stack[0]['size'] == [4, 2]:
#        print("unique:")
#        pprint.pprint(unified_stack)
#        print("not unique:")
#        pprint.pprint(stack)
#        sys.exit("i did something")
    return unified_stack       
    

demo_generator = False         
def generate_all_combinations_slow(upper_blocks, lower_blocks, stack_vertical, border):
    global demo_generator
    if demo_generator: return []
#    if upper_blocks == None or lower_blocks == None or len(upper_blocks) == 0 or len(lower_blocks) == 0:
#        pprint.pprint(upper_blocks)
#        pprint.pprint(lower_blocks)
#        sys.exit("failure, no input_blocks")
    output_blocks = []
    for upper_block in upper_blocks:
        for lower_block in lower_blocks:
            fit_together, stacked_block = stack_2_blocks(upper_block, lower_block, stack_vertical, border)
            if fit_together == True:
                output_blocks.append(stacked_block)
#    if len(output_blocks) > 0:            
#        print("generated", len(output_blocks), output_blocks[0]["size"], "out of", len(upper_blocks), upper_blocks[0]["size"], "and",  len(lower_blocks), lower_blocks[0]["size"] )            
#    return output_blocks
    unified_output = unify_stack_slow(output_blocks)
    if not count_unique_stacks(unified_output):
        print("not unique enough")
        print(unified_output)
    return unified_output      


def append_block(output_blocks, new_block):
    already_in_stack = False
    for i, block in enumerate(output_blocks):        
        if block["outflux"] == new_block["outflux"] and block["influx"] == new_block["influx"]:
            output_blocks[i]["uniqueness"] += new_block["uniqueness"]
            already_in_stack = True
            return output_blocks
    if not already_in_stack:
        output_blocks.append(new_block)  
    return output_blocks        

    
def generate_all_combinations(upper_blocks, lower_blocks, stack_vertical, border):
    global demo_generator
    if demo_generator: return []
#    if upper_blocks == None or lower_blocks == None or len(upper_blocks) == 0 or len(lower_blocks) == 0:
#        pprint.pprint(upper_blocks)
#        pprint.pprint(lower_blocks)
#        sys.exit("failure, no input_blocks")
    output_blocks = []
    for upper_block in upper_blocks:
        for lower_block in lower_blocks:
            fit_together, stacked_block = stack_2_blocks(upper_block, lower_block, stack_vertical, border)
            if fit_together == True:
                output_blocks = append_block(output_blocks, stacked_block)
                #output_blocks.append(stacked_block)
#    if len(output_blocks) > 0:            
#        print("generated", len(output_blocks), output_blocks[0]["size"], "out of", len(upper_blocks), upper_blocks[0]["size"], "and",  len(lower_blocks), lower_blocks[0]["size"] )            
    return output_blocks
    unified_output = unify_stack(output_blocks)
    if not count_unique_stacks(unified_output):
        print("not unique enough")
        print(unified_output)
    return unified_output     

    
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

# checks if uniquifier works
def count_unique_stacks(stacks):
    unique_stacks = []    
    for item in stacks:
        if item not in unique_stacks:
            unique_stacks.append(item)
    
    if len(stacks) != len(unique_stacks):
        print("stackings:", len(stacks), "unique:", len(unique_stacks))
        print("failure. end stack should only have unique items. and did not even count for euqal items with different uniqueness")
        return False
    else: return True    

    
# gives end result: number of combinations    
def count_combinations(stacks):
    counter = 0
    for block in stacks:
        counter += block["uniqueness"]
    return counter

    
# only call this if you want to generate something
def devide_and_conquer(x,y):        
    global counter
    counter = 0     
    global stacks_logger
    stacks_logger = []
    stack = build_up_grid(x,y) 
    unique_stack = stack
#    unique_stack = unify_stack(stack)
    count_unique_stacks(unique_stack) # test if unifier works
    grid_combinations = count_combinations(unique_stack) # calculate end result
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