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
import matplotlib.pyplot as plt

dice = namedtuple("dice", "count sides outcomes label")    
pyramidal = dice(9, [1,2,3,4], [], "pyramidal")
cubical = dice(6, [1,2,3,4,5,6], [], "cubic")
# reduced size
pyramidal = dice(3, [1,2,3,4], [], "pyramidal")
cubical = dice(2, [1,2,3,4,5,6], [], "cubic")
# simple example with one cubic dice on each side
#cubical = dice(1, [1,2,3,4,5,6], [], "cubic")
#pyramidal = dice(1, [1,2,3,4,5,6], [], "cubic")

import itertools

def plotit(data, data2):
    # plot a smoothed line arount the points
    def smooth(plt,x,y,color):
        from scipy.interpolate import spline
        import numpy as np
        
        xnp = np.array(x)
        xnew = np.linspace(xnp.min(),xnp.max(),300)        
        y_smooth = spline(x,y,xnew)        
        plt.plot(xnew,y_smooth, c=color, alpha=0.2)        
        
    with plt.xkcd():

        fig = plt.figure()
    
        x,y = map(list, zip(*data))    
        x2,y2 = map(list, zip(*data2))    
        
        # plot a smoothed line arount the points
        smooth(plt,x,y,"b")
        smooth(plt,x2,y2,"r")       
        
        plt.scatter(x, y, marker = "s", c="b", label = "cubical dices")
        plt.scatter(x2, y2, marker = "v", c="r", label = "pyramidal dices")    
        
        plt.legend(loc="upper left")
        plt.xlabel('Augensumme')
        plt.ylabel('probability')
    
    plt.show()


def probability(eyesum, count, sides):
    if count == 1:
        if ((eyesum > 0) and (eyesum <= sides)):
            return 1/sides
        else:
            return 0
    else:        
        summe = 0
        for i in range(1, eyesum - count + 1 + 1):
            summe += probability(i, 1, sides) * probability(eyesum-i, count-1, sides) 
        return summe    
        

def calc_probability(dice):
    for i in range(dice.count, max(dice.sides)*dice.count + 1):
        dice.outcomes.append([i, probability(i, dice.count, max(dice.sides))])
        

# order of arguments can be swapped to calc loose rate        
def calc_winning_rate(cubical, pyramidal):
    cube_win = 0
    for cubical_throw in cubical.outcomes:
        pyramdial_cummulated_probabilty_if_won = 0
        for pyramidal_throw in pyramidal.outcomes:
            if pyramidal_throw[0] < cubical_throw[0]:
                pyramdial_cummulated_probabilty_if_won += pyramidal_throw[1]
        cube_win += cubical_throw[1] * pyramdial_cummulated_probabilty_if_won

    print(cubical.label,"wins with probability of", cube_win)                
    return cube_win
    

def calc_draw_rate(cubical, pyramidal):   
    draw = 0
    # compare each with each (twice) because of different probabilites (?)
    for cubical_throw in cubical.outcomes:        
        for pyramidal_throw in pyramidal.outcomes:
            if pyramidal_throw[0] == cubical_throw[0]:
                draw += cubical_throw[1] *  pyramidal_throw[1]


    print("draw with probability of", draw)  
    return draw                
        

def solve_problem():
    calc_probability(cubical)
    calc_probability(pyramidal)    
    
    plotit(cubical.outcomes, pyramidal.outcomes)   
    # order of arguments can be swapped to calc loose rate
    win = calc_winning_rate(cubical, pyramidal)    
    loose = calc_winning_rate(pyramidal, cubical)
    draw = calc_draw_rate(pyramidal, cubical)
    
    print("sum of probabilites should at to 1: ", win + loose + draw)
    if (1 - (win + loose + draw)) > 0.0000001: print("sum does not reach around 1")
      
    return 0
    
    
solve_problem()  
print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))

#import profile 
#profile.run('solve_problem()')   

"""
cubic wins with probability of 0.35608975337856585
pyramidal wins with probability of 0.57314407678298
draw with probability of 0.070766169838454
"""