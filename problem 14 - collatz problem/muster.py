# -*- coding: utf-8 -*-
"""
Created on Mon Apr 08 21:48:50 2013

@author: Der_Ventilator
"""

import time

kc = {} # known collatz

def collatz(n):
  cnt = 1
  if n == 1:
    return 1
  if n in kc:
    return kc[n]
  t = 1 + collatz( n/2 if n % 2 == 0 else 3*n+1 )
  kc[n] = t
  return t

st = time.time()
i = 3
highest = 0
m = -1
while i < 1000000:
  c = collatz(i)
  if c > highest:
    highest = c
    m = i
  i += 1

print m,"chain =",highest
print "Elapsed",time.time()-st