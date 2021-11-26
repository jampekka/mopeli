import csv
import itertools
import numpy as np
import random

# TODO: No lane overlap
# TODO: Alternating directions

n_lanes = 7
n_speeds = 7
n_repeats = 1
speed_range = 0.4, 1.4
start_time = 0.5
time_padding = 1
FPS = 60

object_size = 0.075
lane_separation = 2*object_size + object_size*0.1
height = n_lanes*lane_separation

lanes = np.linspace(-height/2, height/2, n_lanes)
speeds = np.linspace(*speed_range, n_speeds)
xs = [-1, 1]
repeats = range(n_repeats)

trials_leftside = []
trials_rightside = []

for repeat, x0, y0, vx0 in itertools.product(repeats, [-1], lanes, speeds):
    vx0 *= -np.sign(x0)
    trials_leftside.append((x0, y0, vx0, 0))
    
for repeat, x0, y0, vx0 in itertools.product(repeats, [1], lanes, speeds):
    vx0 *= -np.sign(x0)
    trials_rightside.append((x0, y0, vx0, 0))    
    
    
#print(",".join(map(str, (lane, y, speed))))
#random.shuffle(trials)

#side = -1**(random.random() < 0.5)
#time = start_time



# pair each left side trial with random right side trial 

# travel distance for ball edge to hit bar edge is less than half screen
s=1- (0.075  + 0.025/2)

paired = []

for i,l in enumerate(trials_leftside):    
    ri = random.randint(0,len(trials_rightside)-1)
    r = trials_rightside.pop(ri)
    pair=[]
    # slower ball is in the first index
    if abs(r[2]) < abs(l[2]):
        pair.append(r)
        pair.append(l)
        
        vslow = r[2]
        vfast = l[2]

    else:
        pair.append(l)
        pair.append(r)
        vslow = l[2]
        vfast = r[2]
        
    tslow = abs(s/vslow)
    tfast = abs(s/vfast)
    
    #delay = 0
    delay = tslow - tfast    #frameratefixtry
    print(delay)
    
    pair.append(delay)
    
    paired.append(pair)
    
    
    
    
random.shuffle(paired)

time = start_time

for a,b,c in paired:
    x0 = a[0]
    y0 = a[1]
    vx0 = a[2]
    vy0 = a[3]
    print(",".join(map(str, (time*1000, x0, y0, vx0, vy0))))
    
    x0 = b[0]
    y0 = b[1]
    vx0 = b[2]
    vy0 = b[3]
    time += c
    print(",".join(map(str, (time*1000, x0, y0, vx0, vy0))))
    
    #speed_in_secs = vx0
    duration = abs(1/vx0)
    time += duration + time_padding
    
    
    
    
    
    
    



# # take trials two at a time, then set timing so that they meet at the center


# for i in range(0,len(trials),2):
#     x0, y0, vx0, vy0 = trials[i]
#     x1, y1, vx1, vy1 = trials[i+1]
#     oldy=y0
#     oldy1=y1
    
    
    
    

# for x0, y0, vx0, vy0 in trials:
#     # Override the direction so they alternate

#     x0 = np.abs(x0)*side
#     vx0 = -np.abs(vx0)*side
#     print(",".join(map(str, (time*1000, x0, y0, vx0, vy0))))
#     speed_in_secs = vx0
#     duration = -x0/speed_in_secs
#     time += duration + time_padding
#     side *= -1


# # Add dummy row so the game doesn't end prematurely
# # 
# #print(",".join(map(str, ((time + 0.3)*1000, 100, y0, vx0, vy0))))
# #block = 
