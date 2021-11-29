import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import sys
import pandas as pd
import scipy.stats

FPS = 60
OBJECT_SIZE = 0.075
LANE_WIDTH = 1/40

def parse_logfile(f, basetime=0.0):
    data = np.loadtxt(f, delimiter=',')

    # From msec to sec
    data[:,0] /= 1000
    data[:,0] += basetime

    # Separate key presses from object starts. These are
    # interleaved in the log.
    keyidx = np.in1d(data[:,1], (888, 999))
    keys = data[keyidx]

    keytimes = keys[:,0]
    keydown = keys[:,1] == 888

    objects = data[~keyidx]

    obj_start_pos = objects[:,1]
    obj_speeds = objects[:,3]
    # Object speeds are in "half-screenwidths per frame". Convert to seconds
    obj_speeds *= FPS
    #obj_speeds *= 1.5

    obj_dur = -obj_start_pos/obj_speeds

    center_hit_times = objects[:,0] + obj_dur
    lead_edge_time = center_hit_times - OBJECT_SIZE/2/np.abs(obj_speeds)
    trail_edge_time = center_hit_times + OBJECT_SIZE/2/np.abs(obj_speeds)

    objects = np.rec.fromarrays(
        (objects[:,0], obj_start_pos, obj_speeds, center_hit_times, lead_edge_time, trail_edge_time, objects[:,2]),
        names="start_time,start_pos,speed,center_hit_time,lead_edge_time,trail_edge_time,ypos")

    min_ttcs = []
    min_ttc_objs = []
    min_ttc_speeds = []

    for keytime in keytimes:
        candidate_idx = np.flatnonzero(objects.trail_edge_time > keytime)
        ttcs = objects[candidate_idx].lead_edge_time - keytime
        min_ttc_idx = np.argmin(ttcs)
        min_ttc = ttcs[min_ttc_idx]
        min_ttc_obj = candidate_idx[min_ttc_idx]
        min_ttcs.append(min_ttc)
        min_ttc_objs.append(min_ttc_obj)
        min_ttc_speeds.append(objects[min_ttc_obj].speed)

    keys = np.rec.fromarrays(
            (keytimes, keydown, min_ttcs, min_ttc_objs, min_ttc_speeds),
            names="time,is_down,min_ttc,min_ttc_obj,min_ttc_speed")
    return objects, keys


allkeys = []
allobjects = []
basetime = 0
for f in sys.argv[1:]:
    objects, keys = parse_logfile(f, basetime)
    objects = pd.DataFrame.from_records(objects)
    #objects['prev_ypos'] = np.nan
    #objects['prev_ypos'].iloc[1:] = objects['ypos'].iloc[:-1]
    #objects['repeatt_ypos'] = False
    objects['repeat_ypos'] = objects['ypos'].diff() == 0
    allobjects.append(objects)
    allkeys.append(pd.DataFrame.from_records(keys))
    basetime = objects.start_time.max() + 1000



keys = pd.concat(allkeys, axis=0).sort_values('time').reset_index()
objects = pd.concat(allobjects, axis=0).sort_values('start_time').reset_index()

#objects = objects[~objects.repeat_ypos]

#plt.plot(objects.start_time.values)
#plt.plot((objects['ypos'] == objects['prev_ypos']).values)

keyups = keys[~keys.is_down]
keydowns = keys[keys.is_down]
#keydowns = keydowns[keydowns.min_ttc < 0.5]

keydowndists = []
for _, obj in objects.iterrows():
    dist = (keydowns.time - obj.start_time)*obj.speed + obj.start_pos #- (OBJECT_SIZE/2 - LANE_WIDTH/2)*np.sign(obj.speed)
    dist = dist[np.abs(dist) < 1]
    dist *= np.sign(obj.speed)
    keydowndists.extend(dist)

objects['keyup_dist'] = np.nan
keyupdists = []
for i, obj in objects.iterrows():
    dist = (keyups.time - obj.start_time)*obj.speed + obj.start_pos #+ (OBJECT_SIZE/2 - LANE_WIDTH/2)*np.sign(obj.speed)
    dist = dist[np.abs(dist) < 1]
    dist *= np.sign(obj.speed)
    try:
        closest = dist[dist < 0.2].idxmax()
        objects.loc[i, 'keyup_dist'] = dist[closest]
    except ValueError:
        pass
        #obj['keyup_dist'] = np.nan
    keyupdists.extend(dist)

#for g, gd in objects.groupby(np.abs(objects.speed)):

objects['keyup_ttc'] = objects['keyup_dist']/np.abs(objects.speed)

for speed, obj in objects.groupby(objects.speed):
    plt.hist(obj.keyup_ttc, histtype='step')
    plt.show()

#plt.hist(objects['keyup_ttc'], bins=30)
#plt.show()

meds = objects.groupby(np.abs(objects.speed))['keyup_dist'].median()

plt.plot(np.abs(objects.speed), objects.keyup_dist, '.', alpha=0.5)

plt.plot(meds)
plt.show()
#pos = objects.speed < 0
#plt.plot(np.abs(objects.speed[pos]), objects.keyup_dist[pos], '.', alpha=0.5)
#plt.plot(np.abs(objects.speed[~pos]), objects.keyup_dist[~pos], '.', alpha=0.5)
#plt.hist(objects.keyup_dist, bins=100)

#plt.hist(keydowndists, bins=100, histtype='step', color='red')
#plt.hist(keyupdists, bins=100, histtype='step', color='green')
plt.show()


