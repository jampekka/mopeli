import csv
import itertools
import numpy as np
import random

# TODO: No lane overlap
# TODO: Alternating directions

n_lanes = 7
n_speeds = 7
n_repeats = 3
speed_range = 0.4, 1.4
start_time = 0.5
FPS = 60

object_size = 0.075
lane_separation = 2*object_size + object_size*0.1
height = n_lanes*lane_separation

lanes = np.linspace(-height/2, height/2, n_lanes)
speeds = np.linspace(*speed_range, n_speeds)
xs = [-1, 1]
repeats = range(n_repeats)

trials = []
for repeat, x0, y0, vx0 in itertools.product(repeats, xs, lanes, speeds):
    vx0 *= -np.sign(x0)
    # The engine expects speeds in frames
    vx0 /= FPS
    trials.append((x0, y0, vx0, 0))
    #print(",".join(map(str, (lane, y, speed))))
random.shuffle(trials)

time = start_time
for x0, y0, vx0, vy0 in trials:
    print(",".join(map(str, (time*1000, x0, y0, vx0, vy0))))
    speed_in_secs = vx0*FPS
    duration = -x0/speed_in_secs
    time += duration

# Add dummy row so the game doesn't end prematurely
print(",".join(map(str, ((time + 0.3)*1000, x0, y0, vx0, vy0))))
#block = 
