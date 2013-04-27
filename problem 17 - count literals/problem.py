# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:30:02 2013

@author: Der_Ventilator

Number	in English	(length)	
0	zero	(4)	
1	one	(3)	
2	two	(3)	
3	three	(5)	
4	four	(4)	
5	five	(4)	
6	six	(3)	
7	seven	(5)	
8	eight	(5)	
9	nine	(4)	
Number	in English	(length)	
10	ten	(3)	
11	eleven	(6)	
12	twelve	(6)	
13	thirteen	(8)	
14	fourteen	(8)	
15	fifteen	(7)	
16	sixteen	(7)	
17	seventeen	(9)	
18	eighteen	(8)	
19	nineteen	(8)	
Number	in English	(length)	
20	twenty	(6)	
21	twentyone	(9)	
22	twentytwo	(9)	
23	twentythree	(11)	
24	twentyfour	(10)	
25	twentyfive	(10)	
26	twentysix	(9)	
27	twentyseven	(11)	
28	twentyeight	(11)	
29	twentynine	(10)	
Number	in English	(length)	
30	thirty	(6)	
31	thirtyone	(9)	
32	thirtytwo	(9)	
33	thirtythree	(11)	
34	thirtyfour	(10)	
35	thirtyfive	(10)	
36	thirtysix	(9)	
37	thirtyseven	(11)	
38	thirtyeight	(11)	
39	thirtynine	(10)	
Number	in English	(length)	
40	forty	(5)	
41	fortyone	(8)	
42	fortytwo	(8)	
43	fortythree	(10)	
44	fortyfour	(9)	
45	fortyfive	(9)	
46	fortysix	(8)	
47	fortyseven	(10)	
48	fortyeight	(10)	
49	fortynine	(9)	
Number	in English	(length)	
50	fifty	(5)	
51	fiftyone	(8)	
52	fiftytwo	(8)	
53	fiftythree	(10)	
54	fiftyfour	(9)	
55	fiftyfive	(9)	
56	fiftysix	(8)	
57	fiftyseven	(10)	
58	fiftyeight	(10)	
59	fiftynine	(9)	
Number	in English	(length)	
60	sixty	(5)	
61	sixtyone	(8)	
62	sixtytwo	(8)	
63	sixtythree	(10)	
64	sixtyfour	(9)	
65	sixtyfive	(9)	
66	sixtysix	(8)	
67	sixtyseven	(10)	
68	sixtyeight	(10)	
69	sixtynine	(9)	
Number	in English	(length)	
70	seventy	(7)	
71	seventyone	(10)	
72	seventytwo	(10)	
73	seventythree	(12)	
74	seventyfour	(11)	
75	seventyfive	(11)	
76	seventysix	(10)	
77	seventyseven	(12)	
78	seventyeight	(12)	
79	seventynine	(11)	
Number	in English	(length)	
80	eighty	(6)	
81	eightyone	(9)	
82	eightytwo	(9)	
83	eightythree	(11)	
84	eightyfour	(10)	
85	eightyfive	(10)	
86	eightysix	(9)	
87	eightyseven	(11)	
88	eightyeight	(11)	
89	eightynine	(10)	
Number	in English	(length)	
90	ninety	(6)	
91	ninetyone	(9)	
92	ninetytwo	(9)	
93	ninetythree	(11)	
94	ninetyfour	(10)	
95	ninetyfive	(10)	
96	ninetysix	(9)	
97	ninetyseven	(11)	
98	ninetyeight	(11)	
99	ninetynine	(10)	
100	hundred	(7)
"""

def count(string):
    return len(string)
    

#count('one')
wordscount = 1000

#will contain literals without spaces or hyphens (-)
word = [0 for x in range(wordscount+1)]

#1..13
word[1] = 'one'
word[2] = 'two'
word[3] = 'three'
word[4] = 'four'
word[5] = 'five'
word[6] = 'six'
word[7] = 'seven'
word[8] = 'eight'
word[9] = 'nine'
word[10] = 'ten'
word[11] = 'eleven'
word[12] = 'twelve'
word[13] = 'thirteen'

#14..19
teen = 'teen'

for i in range(14,19+1):
    word[i] = word[i-10]+teen
    #print word[i]

#fixes
word[15] = 'fif'  +teen
word[18] = 'eigh' +teen
    
#20..99    

#will contain decas 20,30,40,50..90
deca = [0 for x in range(10)]

deca[2] = 'twenty'
deca[3] = 'thirty'

ty = 'ty'
for i in range(4,9+1):
    deca[i] = word[i]+ty
    #print deca[i]
    
#fixes
deca[5] = 'fif'  +ty
deca[4] = 'for'  +ty
deca[8] = 'eigh' +ty    



#add decas with 1...9
for i in range(20,99+1):
    if i % 10 == 0:
        word[i] = deca[i // 10]
    else:
        word[i] = deca[i // 10] + word [i % 10]
    #print word[i]    
    
#100..

#gather 100,200,300
hundred = 'hundred'    
strand  = 'and'
hund = [0 for x in range(10)]

for i in range(1,10):
    hund[i] = word[i] + hundred
    #print hund[i]

for i in range(100,999+1):
    if i % 100 == 0:
        word[i] = hund[i // 100]
    else:
        word[i] = hund[i // 100] + strand + word [i % 100]
    #print word[i]    

word[1000] = 'onethausend'
summe = 0    

for i in range(1,1000+1):
    summe += len(word[i]) 
    print i, word[i]
 
print summe   