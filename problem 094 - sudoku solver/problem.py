# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:08:04 2015

@author: gruenewa



Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.


A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.

The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.

"""

import profile
import copy

database_filename = 'p096_sudoku.txt'
dimension = 9
empty_sudoku = [[0]*dimension for i in range(dimension)]
digits = set(i+1 for i in range(9))

def import_database(filename):
    f = open(filename,'r')
    content = []
    j = 0 # lines
    for line in f:
        if line[0] == "G": # keyword in file = "Grid XX"
            content.append(empty_sudoku)
            j = 0
        else:            
            for i, digit in enumerate(str.strip(line)): # i are lines
                content[-1][j][i] = int(digit)
            j += 1    
    return content
    
def solve_sudoku(sudoku):
    pristine_sudoku = copy.deepcopy(sudoku)  
    
    #run over each element
    for i in range(9):
        for j in range(9):
            # change item if not yet converted to a set of possible numbers, e.g. is pristine
            if sudoku[j][i] == 0:
                # check number of possible solutions for that item
                possible_digits = set.copy(digits)
                for search_i in range(9):
                    possible_digits.discard(sudoku[j][search_i])
                for search_j in range(9):
                    possible_digits.discard(sudoku[search_j][i])  
                sudoku[j][i] = possible_digits
                
    for i, lines in enumerate(sudoku):
        print(lines)            
        print(pristine_sudoku[i])
    
def solve_problem():     
    database = import_database(database_filename)
    solve_sudoku(database[0])
         
 
    
solve_problem()   
# profile.run('solve_problem()') 