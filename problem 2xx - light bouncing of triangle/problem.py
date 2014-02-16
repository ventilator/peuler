# -*- coding: utf-8 -*-
"""
Created on Sat Feb 01 21:55:01 2014

@author: ventilator
"""
alpha = 10

def do_stuff():
    
    
    beta = C()+A()+B()+C()+A()+C()+B()+C()+A()+B()+C()
    print beta % 360
    
    return 0

def C():
    return (360-2*alpha)
    
def B():
    return (alpha-60)

def A():
    return (60-alpha)

do_stuff()