# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 16:07:11 2015

@author: venti

Peter has nine four-sided (pyramidal) dice, each with faces numbered 1, 2, 3, 4.
Colin has six six-sided (cubic) dice, each with faces numbered 1, 2, 3, 4, 5, 6.

Peter and Colin roll their dice and compare totals: the highest total wins. The result is a draw if the totals are equal.

What is the probability that Pyramidal Pete beats Cubic Colin? Give your answer rounded to seven decimal places in the form 0.abcdefg

"""
"""
Problem can be reduced to 3 dice for Peter and 2 dice for colin? no, because discrete Problem. (probably correct)
Mediumvaluecomparison would not change but draws are not accounted for - > more draws?
But: solve first for 3 vs 2 dice for easyness (+possible check if answer is correct. if yes --> done)


"""
import time
start_time = time.time()        
    
from collections import namedtuple

dice = namedtuple("dice", "count sides outcomes")    
pyramidal = dice(9, [1,2,3,4], [])
cubical = dice(6, [1,2,3,4,5,6], [])
# reduced size
pyramidal = dice(3, [1,2,3,4], [])
cubical = dice(2, [1,2,3,4,5,6], [])

import itertools

def solve_problem():
    print(pyramidal.count)
    pyramidal.outcomes.append(list(itertools.product(pyramidal.sides, repeat=pyramidal.count)))
    pyramidal.outcomes.append(list(map(sum, pyramidal.outcomes)))
    print(pyramidal.outcomes)
        
    return 0
    
    
solve_problem()  
print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))

#import profile 
#profile.run('solve_problem()')   