# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:59:56 2015

@author: gruenewa
"""

def tri(n):
    return n*(n+1)/2

def pen(n):
    return n*(3*n-1)/2

def hexa(n):
    return n*(2*n-1)


def main():
    max_n = 100000
    lut_tri = set()
    lut_pen = set()
    lut_hexa = set()

    for i in range(1,max_n):
        lut_tri.add(tri(i))
        lut_pen.add(pen(i))
        lut_hexa.add(hexa(i))

    lut_result = lut_pen & lut_tri & lut_hexa
    print(lut_result)

main()