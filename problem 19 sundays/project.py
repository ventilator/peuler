# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 23:11:31 2013

@author: ventilator

You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
"""

startyear = 1901
stopyear  = 2000

daysinmonth = [31,28,31,30,31,30,31,31,30,31,30,31]

#sunday = 7 
#monday = 1
weekday = 1
day   = 1
month = 0 #januar
year  = 1900
sundays = 0


while year <= stopyear:
    if year >= startyear and day == 1 and weekday % 7 == 0:
        sundays += 1
        print day,month,year,sundays


    weekday += 1  
        
    day = (day + 1)
    
    if day > daysinmonth[month]:
        day = 1
        month += 1
        if month > 11:
            month = 0
            year += 1
            if year % 4 == 0 and year % 100 == 0 and year % 400 != 0:
                daysinmonth[1] = 29
            else:
                daysinmonth[1] = 28
           
    #print day,month,year
    
    

  