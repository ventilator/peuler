# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014
@author: ventilator 


best practice:
    hashable, immutable datatypes are your friend. no need for deepcopy etc, faster


"""

import time
start_time = time.time()        
    

def solve_problem():
           
    return 0
    
    
solve_problem()  
print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))

#import profile 
#profile.run('solve_problem()')   