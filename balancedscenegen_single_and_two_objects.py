import csv
import itertools
import numpy as np
import random

"""
"- Interleave single and two objects
- Both objects from same side, alternating sides
- About half screen y range
- "Trial types"
  - Single object trials
  - Two objects: same speed, same start
  - Two objects: same ttc, different speed
  - Two objects: different ttc
    - 0.1, 0.2, 0.3 differences
    - "Confounding ball" comes later (higher TTC)
- Use lanes for y diff
- Uniform lane distribution
- About 100 trials per block
- Stratify speeds to the 7 levels
- Three repetitions per speed
  - Leads to 126
"""


n_lanes = 4
n_speeds = 7
n_repeats = 3
speed_range = 0.4, 1.4
start_time = 0.5
time_padding = 0.3
FPS = 60

object_size = 0.075
bar_width = 0.025

lane_separation = 2*object_size + object_size*0.1
height = n_lanes*lane_separation

lanes = np.linspace(-height/2, height/2, n_lanes)
speeds = np.linspace(*speed_range, n_speeds)

xs = [-1, 1]
repeats = range(n_repeats)

ttcs = [0, 0.1, 0.2, 0.3]

trials_different_speeds = []

# travel distance for ball edge to hit bar edge is less than half screen
s=1- (object_size/2  + bar_width/2)



# different speeds

pairs_speed_and_times = []

for vx0, ttc in itertools.product(speeds, ttcs):
    
    # first ball travel time at set speed
    t0 = abs(s/vx0)
    
    # select second ball speed randomly and different than vx0 
    vx0_2 = random.choice([v for v in speeds if v!=vx0])
        
    # second ball arrives at center at time=ttc later than the target ball
    # delay can be negative too .. 
    
    t2 = abs(s/vx0_2)    
    t2_delay = t0 + ttc - t2
    
    # if delays is negative, ball 2 goes first
    
    if t2_delay < 0:
        pairs_speed_and_times.append([vx0_2, vx0, -t2_delay])
    else:
        pairs_speed_and_times.append([vx0,vx0_2,t2_delay])


# same speed, same ttc       

# single trials
    
pairs_same_speed = []
single_speeds = []
for vx0 in speeds:
    pairs_same_speed.append([vx0,vx0,0] )
    single_speeds.append([vx0,0,0])
    





all_pairs = single_speeds + pairs_same_speed + pairs_speed_and_times

all_pairs *= n_repeats

n_total = len(all_pairs)


# balancing lanes.. we creates stack of lanes to choose from 

replanes = np.ceil(n_total/n_lanes)
lanes_stack = np.repeat(lanes,replanes)
random.shuffle(lanes_stack)
lanes_stack = list(lanes_stack)



time = start_time

random.shuffle(all_pairs)

x0 = -1 
for (vx0,vx0_2,delay) in all_pairs:  
    x0 *=-1    
    y0 = lanes_stack.pop()
    vx0 *= -1*x0
    vy0 = 0    
    print(",".join(map(str, (time*1000, x0, y0, vx0, vy0))))
    duration = duration = abs(s/vx0)
    
    # if we have a second ball:
    if vx0_2 > 0:
        time += delay
        # second ball on random lane different than the first one
        y0_2 = random.choice([l for l in lanes if l!=y0])
        vx0_2 *= -1*x0
        vy0_2 = 0        
        print(",".join(map(str, (time*1000, x0, y0_2, vx0_2, vy0))))
        duration = abs(s/vx0_2)
    time += duration + time_padding
    
    
    
    
    
    