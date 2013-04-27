# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 20:21:59 2013

@author: Der_Ventilator

problem 18 with loadfromfile
"""


def printtriangle(num):
    for i in num:
        line = ''
        for j in i:
            line +=' ' + str(j).zfill(2) + ' '        
        print str(line).center(80,' ')   
        
def printtriangleback(num):
    for i in reversed(num):
        line = ''
        for j in i:
            line +=' ' + str(j).zfill(3) + ' '        
        print str(line).center(80,' ')           


filename = 'triangle.txt'
f = open(filename,'r')
numstr = []

for line in f:
    numstr.append(line.rstrip('\r\n'))

f.close()    
'''
linecount = 15
numstr = ['' for x in range(linecount) ]

numstr[0] = '75'
numstr[1] = '95 64'
numstr[2] = '17 47 82'
numstr[3] = '18 35 87 10'
numstr[4] = '20 04 82 47 65'
numstr[5] = '19 01 23 75 03 34'
numstr[6] = '88 02 77 73 07 63 67'
numstr[7] = '99 65 04 28 06 16 70 92'
numstr[8] = '41 41 26 56 83 40 80 70 33'
numstr[9] = '41 48 72 33 47 32 37 16 94 29'
numstr[10] = '53 71 44 65 25 43 91 52 97 51 14'
numstr[11] = '70 11 33 28 77 73 17 78 39 68 17 57'
numstr[12] = '91 71 52 38 17 14 91 43 58 50 27 29 48'
numstr[13] = '63 66 04 68 89 53 67 30 73 16 69 87 40 31'
numstr[14] = '04 62 98 27 23 09 70 98 73 93 38 53 60 04 23'
'''

#int list
num = [ [0 for y in range(0,x+1)] for x in range(len(numstr)) ]



#convert in int array with single sites
for i in range(len(numstr)):
    itemsinline = (i+1)
    for j in range(itemsinline):
        num[i][j] = int(numstr[i][j*3] + numstr[i][j*3+1])
    #num[i] = 
    
printtriangle( num )    

#list with directions to go
#directions = [ [0 for y in range(0,x+1)] for x in range(linecount) ]
#printtriangle ( directions )
calcnum = num
#printtriangleback( calcnum )

for i in range(len(calcnum)-1,0,-1):
    for j in range(len(calcnum[i])-1):
        if calcnum[i][j] > calcnum[i][j+1]:
            calcnum[i-1][j] += calcnum[i][j]
        else:
            calcnum[i-1][j] += calcnum[i][j+1]
            
        
    
printtriangleback( calcnum )