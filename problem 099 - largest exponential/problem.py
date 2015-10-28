# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator
"""

import profile
import time
import pprint
import math
        
    
filename = "p099_base_exp.txt"

def read_file(filename):
    f = open(filename)
    db = []
    for line in f:
        line = line.strip()
        db.append(line.split(","))

    for i, line in enumerate(db):
        for j, item in enumerate(line):
            db[i][j] = int(db[i][j])
    
    return db


def calculate(db):
    max_i = -1
    max_log = 0
    for i, line in enumerate(db):
       base = db[i][0]
       exponent = db[i][1]
       logarithm = exponent * math.log(base)
       line.append(logarithm)
       if logarithm > max_log:
           max_log = logarithm
           max_i = i
           
    return max_i + 1       
        
        

def solve_problem():
    db = read_file(filename)    
    max_line = calculate(db)
    pprint.pprint(db)
    
    print("maximum in line",max_line)
    
    return 0
    
    
    
    
    
start_time = time.time()

solve_problem()  

print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))
 
# profile.run('solve_problem()')   