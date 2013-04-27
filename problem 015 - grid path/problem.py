# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 22:21:09 2013

@author: Der_Ventilator
"""

#''' first (and second with wall optimazitation) try which takes too long (>2min)
'''
gridsize = 20
for gridsize in range(2, gridsize+1):    
    routes = 0
    startx = 0
    starty = 0
    print 'x','y'
    
    def increase(x,y):
        #print x,y
        
        

        #wenn an einer Wand, dann gibts eh nur noch einen Weg (spart nicht viel)    
        if (x == gridsize) or (y==gridsize):
            global routes
            routes +=1
            
            #print '----'
            return
            
        if (x > gridsize) or (y > gridsize):    
            print 'this should not happen'
            
        if (x < gridsize):
            increase(x+1,y)
        if (y < gridsize):    
            increase(x,y+1)            
            
    increase( startx, starty )     
    print 'routes'   
    print gridsize, routes
'''    
    
    
''' 
with some thinking i need to bulid this

            1^2
        1^2  +  1^2
    1^2  +  2^2  +  1^2
1^2  +   3^2 +  3^2  +  1^2    
'''    
def squareandsum ( numbers ):
    sumation = 0
    for i in numbers:
        sumation += i*i
    return sumation    

'''
numbers = [1]
print numbers, squareandsum ( numbers )
numbers = [1,1]
print numbers, squareandsum ( numbers )
numbers = [1,2,1]
print numbers, squareandsum ( numbers )
'''


def nextstep (numbers):
    #erzeuge "leeres" array
    newnumbers = [0 for x in range(len(numbers)+1)]
    #print newnumbers
    
    for i in range(0,len(numbers)-1):
        #print i
        newnumbers[i+1] = numbers[i] + numbers[i+1]
   
    return newnumbers   

print "squares, [], routes"
#startbaum
numbers = [0,1,0]
for i in range(1,22):
    print i-1, numbers, squareandsum ( numbers )
    numbers = nextstep(numbers) 
    
    
'''after 1 sec it gives solution
squares, [], routes
0 [0, 1, 0] 1
1 [0, 1, 1, 0] 2
2 [0, 1, 2, 1, 0] 6
3 [0, 1, 3, 3, 1, 0] 20
4 [0, 1, 4, 6, 4, 1, 0] 70
5 [0, 1, 5, 10, 10, 5, 1, 0] 252
6 [0, 1, 6, 15, 20, 15, 6, 1, 0] 924
7 [0, 1, 7, 21, 35, 35, 21, 7, 1, 0] 3432
8 [0, 1, 8, 28, 56, 70, 56, 28, 8, 1, 0] 12870
9 [0, 1, 9, 36, 84, 126, 126, 84, 36, 9, 1, 0] 48620
10 [0, 1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1, 0] 184756
11 [0, 1, 11, 55, 165, 330, 462, 462, 330, 165, 55, 11, 1, 0] 705432
12 [0, 1, 12, 66, 220, 495, 792, 924, 792, 495, 220, 66, 12, 1, 0] 2704156
13 [0, 1, 13, 78, 286, 715, 1287, 1716, 1716, 1287, 715, 286, 78, 13, 1, 0] 10400600
14 [0, 1, 14, 91, 364, 1001, 2002, 3003, 3432, 3003, 2002, 1001, 364, 91, 14, 1, 0] 40116600
15 [0, 1, 15, 105, 455, 1365, 3003, 5005, 6435, 6435, 5005, 3003, 1365, 455, 105, 15, 1, 0] 155117520
16 [0, 1, 16, 120, 560, 1820, 4368, 8008, 11440, 12870, 11440, 8008, 4368, 1820, 560, 120, 16, 1, 0] 601080390
17 [0, 1, 17, 136, 680, 2380, 6188, 12376, 19448, 24310, 24310, 19448, 12376, 6188, 2380, 680, 136, 17, 1, 0] 2333606220
18 [0, 1, 18, 153, 816, 3060, 8568, 18564, 31824, 43758, 48620, 43758, 31824, 18564, 8568, 3060, 816, 153, 18, 1, 0] 9075135300
19 [0, 1, 19, 171, 969, 3876, 11628, 27132, 50388, 75582, 92378, 92378, 75582, 50388, 27132, 11628, 3876, 969, 171, 19, 1, 0] 35345263800
20 [0, 1, 20, 190, 1140, 4845, 15504, 38760, 77520, 125970, 167960, 184756, 167960, 125970, 77520, 38760, 15504, 4845, 1140, 190, 20, 1, 0] 137846528820'''    