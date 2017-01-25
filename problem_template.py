# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014
@author: ventilator 


best practice:
    hashable, immutable datatypes are your friend. no need for deepcopy etc, faster and safer
    use Counter or NamedTuple for clean code


"""

def solve_problem():
           
    return 0
    
if __name__ == "__main__":    
    import time
    start_time = time.time()         
    solve_problem()  
    print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))

#import profile 
#profile.run('solve_problem()')   