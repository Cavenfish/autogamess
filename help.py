"""
This file contains multiple small helper functions for the pyGAMESS module.

The following functions are in this file:

    ctr_f: similar to computer find tool (control f)

    ctr_f_all: similar to computer find all tool

    angle_between: finds the angle between two vectors using the dot product
    formula (u \dot v = |u| |v| cos\theta )

    get_bond_data: finds the bond lengths and angles, returns a
    DataFrame with these values

"""
import numpy as np


def ctr_f(find_this, look_here):
    for line in look_here:
        if find_this in line:
            return look_here.index(line)
    return -1

def angle_between(v1, v2):
    normv1 = v1 / np.linalg.norm(v1)
    normv2 = v2 / np.linalg.norm(v2)
    return np.arccos(np.dot(v1,v2) / (normv1 * normv2))

def ctr_f_allR(find_this, look_here):
    r = []
    for line in look_here:
        if 'TERMINATED -ABNORMALLY-' in line:
            r.append('N/A')
            r.append('N/A')
        if find_this in line:
            r.append(line.split(':')[1])
    return r
