#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 15:42:01 2021

@author: t
"""

import csv
from random import random, choice


def writelog(*args):
    with open(filename, 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(args)
     
        
filename = 'singles.csv'
open(filename, 'w').close()   #empty file


time = 500  #  time start in ms
vx0=1

scale = 20 

for i in range(100):
    time = time + ( scale / abs(vx0))  # time when previous ball crosses center
    x0 = choice([-1,1])  
    y0 = choice([-1,1])*random()    
    vx0 = -x0 * (random()/80 + 0.01)
    vy0 = 0
    writelog(time,x0,y0,vx0,vy0)
    
    
