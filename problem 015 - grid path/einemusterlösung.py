# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 23:58:56 2013

@author: Der_Ventilator
"""

paths = { (20, 20) : 1 } 
print paths

def do_path(x, y): 
    if (x, y) in paths:
        return paths[(x, y)] 
    results = 0 
    if x < 20: 
        results += do_path(x + 1, y)
    if y < 20: 
        results += do_path(x, y + 1)
    paths[(x, y)] = results
    return results

print do_path(0, 0)