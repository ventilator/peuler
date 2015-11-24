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

dice = namedtuple("dice", "count sides outcomes")    
pyramidal = dice(9, [1,2,3,4], [])
cubical = dice(6, [1,2,3,4,5,6], [])
# reduced size
pyramidal = dice(3, [1,2,3,4], [])
cubical = dice(2, [1,2,3,4,5,6], [])

import itertools

def plotit(data, data2):
    with plt.xkcd():
    # Based on "Stove Ownership" from XKCD by Randall Monroe
    # http://xkcd.com/418/

        fig = plt.figure()
#        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
#        ax.spines['right'].set_color('none')
#        ax.spines['top'].set_color('none')
#        plt.xticks([])
#        plt.yticks([])
#        ax.set_ylim([-30, 10])
#    
#        data = np.ones(100)
#        data[70:] -= np.arange(30)
    
#        plt.annotate(
#            'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
#            xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))
    
        x,y = map(list, zip(*data))    
        x2,y2 = map(list, zip(*data2))    
        
        plt.scatter(x, y, marker = "s", c="b", label = "cubical dices")
        plt.scatter(x2, y2, marker = "v", c="r", label = "pyramidal dices")    
        
        plt.legend(loc="upper left")
        plt.xlabel('Augensumme')
        plt.ylabel('probability')
#        fig.text(
#            0.5, 0.05,
#            '"Stove Ownership" from xkcd by Randall Monroe',
#            ha='center')
    
        # Based on "The Data So Far" from XKCD by Randall Monroe
        # http://xkcd.com/373/
    
#        fig = plt.figure()
#        ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
#        ax.bar([-0.125, 1.0-0.125], [0, 100], 0.25)
#        ax.spines['right'].set_color('none')
#        ax.spines['top'].set_color('none')
#        ax.xaxis.set_ticks_position('bottom')
#        ax.set_xticks([0, 1])
#        ax.set_xlim([-0.5, 1.5])
#        ax.set_ylim([0, 110])
#        ax.set_xticklabels(['CONFIRMED BY\nEXPERIMENT', 'REFUTED BY\nEXPERIMENT'])
#        plt.yticks([])
#    
#        plt.title("CLAIMS OF SUPERNATURAL POWERS")
#    
#        fig.text(
#            0.5, 0.05,
#            '"The Data So Far" from xkcd by Randall Monroe',
#            ha='center')
    
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
        

def solve_problem():
    calc_probability(cubical)
    calc_probability(pyramidal)    
    
    
     
    # plotit(pyramidal.outcomes)
    # plotit(cubical.outcomes)
    plotit(cubical.outcomes, pyramidal.outcomes)    
    # pyramidal.outcomes.append(list(map(sum, pyramidal.outcomes)))
    # print(pyramidal.outcomes)
        
    return 0
    
    
solve_problem()  
print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))

#import profile 
#profile.run('solve_problem()')   