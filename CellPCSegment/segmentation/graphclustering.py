import numpy as np
from skimage.measure import profile_line
from collections import deque

def get_neighbours(point, len_d1, len_d2):
    d1, d2 = point

    nbhrs = []

    if d1-1 >= 0:
        nbhrs.append((d1-1, d2))
    
    if d1+1 < len_d1:
        nbhrs.append((d1+1, d2))
    
    if d2-1 >= 0:
        nbhrs.append((d1, d2-1))
    
    if d2+1 < len_d2:
        nbhrs.append((d1, d2+1))

    return nbhrs

def unvisited_point(point, seg_mask):
    d1, d2 = point

    if seg_mask[d1, d2] == 0:
        return True

    return False

def propagate(image, colordim=0, colorthres=50):
    image = np.flip(image, axis=0)
    len_d1, len_d2 = image.shape[:2]

    prop_seeds = [(0,0),(0,len_d2-1),(len_d1-1,0),(len_d1-1,len_d2-1)]

    seg_mask = np.zeros((len_d1,len_d2))
    seg_mask[image[:,:,colordim] >= colorthres] = 125 #lbl line

    #visited = np.zeros((len_d1,len_d2))
    #seg_mask[image[:,:,colordim] >= colorthres] = 125
    for i, initseed  in enumerate(prop_seeds):
        print(i)
        nextseed = deque()
        nextseed.append(initseed)

        while len(nextseed) > 0:
            #if len(nextseed) %1000 == 0:
            #    print(len(nextseed))

            s = nextseed.pop()
            d1, d2 = s

            seg_mask[d1, d2] = i+1

            for nbr in get_neighbours(s, len_d1, len_d2):
                #if unvisited_point(nbr):
                if seg_mask[nbr[0], nbr[1]] == 0:
                     nextseed.append(nbr)
    
    return seg_mask
