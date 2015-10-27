# -*- coding: utf-8 -*-
"""
@author: venti


Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.


A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.

The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.

"""

import profile
import time
import copy

database_filename = 'p096_sudoku.txt'
dimension = 9
empty_sudoku = [[0]*dimension for i in range(dimension)]
digits = set(i+1 for i in range(9))

superlatice_dimension = dimension // 3

verbose = False

# lame creation of superlatice, since 2D init of array of sets somehow fails with deep copy
filled_superlatice = []
for j in range(superlatice_dimension):
    filled_superlatice.append([copy.deepcopy(digits), copy.deepcopy(digits), copy.deepcopy(digits)])
        

def import_database(filename):
    f = open(filename,'r')
    content = []
    j = 0 # lines
    for line in f:
        if line[0] == "G": # keyword in file = "Grid XX"
            content.append(copy.deepcopy(empty_sudoku))
            j = 0
        else:            
            for i, digit in enumerate(str.strip(line)): # i are lines
                if int(digit) == 0: # I want no 0s but all possible digits
                    content[-1][j][i] = copy.deepcopy(digits)
                else:                    
                    content[-1][j][i] = set([int(digit)])
            j += 1    
    return content

print_item_x = 4
print_item_y = 0
    
def solve_sudoku(unsolved_sudoku, recursion_depth = 1):
    
    sudoku = copy.deepcopy(unsolved_sudoku)
    
    sudoku_superlatice = copy.deepcopy(filled_superlatice) # contains numbers to be distributed until len()=0    
    
    for times in range(81):    
        # save state from round before
        pristine_sudoku = copy.deepcopy(sudoku)
        pristine_superlatice = copy.deepcopy(sudoku_superlatice)
        
        # run over each element
        for i in range(dimension): # i = x
            for j in range(dimension): # j = y
                # change item if not yet converted to a set of possible numbers, e.g. is pristine
                if len(sudoku[j][i]) > 1:
    
                    # check number of possible solutions for that item
                    possible_digits = copy.deepcopy(digits)
                    # search with fixed y = search in x direction
                    for search_i in range(dimension):
                        current_item = copy.deepcopy(sudoku[j][search_i])
                        if len(current_item) == 1:
                            possible_digits.difference_update(current_item)
                    # search with fixed x = search in y direction
                    for search_j in range(dimension):
                        current_item = copy.deepcopy(sudoku[search_j][i])                    
                        if len(current_item) == 1:
                            possible_digits.difference_update(current_item)                 
                    # update immediately   
                    sudoku[j][i].intersection_update(possible_digits)

                    
                    # check if given possible numbers are also available in supercell
                    # if not, then number must be for that cell (e.g. a 4 has to be in this cell because all other cells are forbidden)
                    
                    # calculate cell boundary
                    i0 = (i // superlatice_dimension) * superlatice_dimension       
                    j0 = (j // superlatice_dimension) * superlatice_dimension 

                    # gather all allowed digits
                    other_locations_allow = set()                    
#                    other_locations_allow.clear()
#                    this_location_may = set()
#                    this_location_may.clear()
                    
                    for i_i in range(i0, i0 + superlatice_dimension):
                            for j_j in range(j0, j0 + superlatice_dimension):
                                if not (i_i == i and j_j == j):
                                    other_locations_allow.update(sudoku[j_j][i_i])
                    
                    # if something remains, which is not allowed on other locations
                    this_location_may = copy.deepcopy(sudoku[j][i])
                    this_location_may.difference_update(other_locations_allow)     
                    if len(this_location_may) == 1:
                        sudoku[j][i].intersection_update(this_location_may)
                       
    
                else: # look at numbers which are to some extend crunched down    
                    pass
                
                # search for superlatice
                superlatice_x = i // 3
                superlatice_y = j // 3   
                    
                if len(sudoku[j][i]) == 1: # if item already solved discard from superlatice
                    sudoku_superlatice[superlatice_y][superlatice_x].difference_update(sudoku[j][i])
                    
                # 3rd sudoko method: look at superlatice grid    
                # superlatice contains now possible numbers to distribute into latice
                # take possible digits, intersect with superlatice
                if len(sudoku[j][i]) != 1:
                    sudoku[j][i].intersection_update(sudoku_superlatice[superlatice_y][superlatice_x])
    
        # print_sudoku(pristine_sudoku, sudoku, False)                

        # print("round: " + str(times))        
        if pristine_sudoku == sudoku and pristine_superlatice == sudoku_superlatice:
            if verbose: print("Solution attempt took", times, "rounds")
            # check for candidates to maybe check recursivly
            if recursion_depth > 0:
                recursion_depth -= 1
                for y, lines in enumerate(sudoku):
                    for x, items in enumerate(lines):
                        if len(items) == 2:
                            # print(y,x,items)
                            for possible_item in items:
                                test_sudoku = copy.deepcopy(sudoku)
                                test_sudoku[y][x] = set([possible_item])
                                if verbose: print("testing a guess")
                                test_sudoku = solve_sudoku(test_sudoku, recursion_depth)
                                if verify_sudoku(test_sudoku):
                                    return test_sudoku
                        
            # break
            return sudoku        


def print_sudoku(before, after, current_state = True):

    print('─────┼before─────┼┼─────┼after┼─────┼─')
    print('─────┼─────┼─────┼┼─────┼─────┼─────┼─')
    
    for j, lines in enumerate(after):
        print_string_after = ''
        print_string_before = ''
        
        for i, item in enumerate(lines):
            to_print = str(item)
            if current_state == False:                
                if len(item) != 1: # do not print multiple choices
                    to_print = ' ' 
                else:
                    to_print = to_print[1]

            item_length = len(to_print)                     
            # add color if item is different        
            if item != before[j][i]:
                to_print = '\x1b[1;31m' + to_print + '\x1b[0m'                    
            if (i+1) % 3 == 0:
                seperator = '│'
            else:
                seperator= ' '
            print_string_after += to_print + seperator
            
            # before line
            item = before[j][i]
            to_print = str(before[j][i])
            # insert lines
            if current_state == False:                
                if len(item) != 1: # do not print multiple choices
                    to_print = ' ' 
                else:
                    to_print = to_print[1]                
            if (i+1) % 3 == 0:
                seperator = '│'
            else:
                seperator= ' '
            
            print_string_before += to_print + ' '*(item_length - len(to_print) )  + seperator
            
        if current_state:    
            print(print_string_after)
            print(print_string_before)        
        else:
            print(print_string_before + '│' + print_string_after)
        if (j+1) % 3 == 0:
            print('─────┼─────┼─────┼┼─────┼─────┼─────┼─')
        

# does not verifiy block structure
def verify_sudoku(sudoku):
    is_valid = True
    
    complete_line = copy.deepcopy(digits)
    row_check = [complete_line for i in range(dimension)]
    
    for lines in sudoku:
        complete_line = copy.deepcopy(digits)
        for i, item in enumerate(lines):
            if len(item) == 1:
                complete_line.discard(item)
                row_check[i].discard(item)
            else:
                is_valid = False
        if not complete_line: # if empty
            is_valid = False
    
    for row in row_check:
        if not row:
            is_valid = False            
     
    return is_valid       
        
    
def solve_problem():     
    database = import_database(database_filename)
    solved_database = copy.deepcopy(database)
    valid_solutions = 0
    invalid_solutions = 0    
    
    hard_cases = [5, 41, 43, 48] # experimental observation
    
    for i, sudokus in enumerate(database):
        if i in hard_cases: # number of guesses to test out until stopping to try
            recursion_depth = 2
        else:
            recursion_depth = 1
            
        print("Solving item",i,"...")
        solved_database[i] = solve_sudoku(database[i], recursion_depth)
        print_sudoku(database[i], solved_database[i], False)
        if not verify_sudoku(solved_database[i]):
            print('\x1b[1;33m'+'Solution is invalid'+'\x1b[0m')
            invalid_solutions += 1                
        else:
            print("Solution is valid")
            valid_solutions += 1
            
    print(valid_solutions, "valid solitions.", invalid_solutions, "invalid solutions.", valid_solutions+invalid_solutions, "in total." )       
    if verbose: print("hard cases are", hard_cases)
    
    get_solution_for_peuler(solved_database)
         

def get_solution_for_peuler(solved_sudokus):
    sums = []
    for sudoku in solved_sudokus:
        sums.append(list(sudoku[0][0])[0]*100 + list(sudoku[0][1])[0]*10 + list(sudoku[0][2])[0])
    
    print(sums[0], "should be 483 (verification)")
    print(sum(sums), "should be the correct answer for peuler.")    




start_time = time.time()

solve_problem()  

print("--- %s seconds ---" % (time.time() - start_time))

# profile.run('solve_problem()') 

# profiling does take very long. Normal run takes <30 seconds
# better guessing algorithm might help which testrun to do. so far just testing by occurence