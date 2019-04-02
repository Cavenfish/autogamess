"""
This file contains multiple small helper functions for the pyGAMESS module.

The following functions are in this file:

    ctr_f: similar to computer find tool (control f)

    angle_between: finds the angle between two vectors using the dot product
    formula (u \dot v = |u| |v| cos\theta )

    make_xzy: turns a list of xyz values into a float tuple of xyz

"""
import numpy as np


def ctr_f(find_this, look_here):
    for line in look_here:
        if find_this in line:
            return look_here.index(line)
    return -1

def angle_between(v1, v2):
    v1hat = v1 / np.linalg.norm(v1)
    v2hat = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1hat, v2hat), -1.0, 1.0))

def make_xzy(xyzlist):
    r = (float(xyzlist[0]),
         float(xyzlist[0]),
         float(xyzlist[0]))
    return r
