"""
This is the autogamess module, a python module designed to automate
optimization, hessian, raman, and VSCF input generation and output
data collection.

Contains the following functions:
                bat_maker
                new_project
                opt2hes
                sort_logs
                hes2raman
                get_data


Author: Brian C. Ferrari
"""
import os
import numpy  as np
import pandas as pd

from .bat_maker   import bat_maker
from .new_project import new_project
from .opt2hes     import opt2hes
from .sort_logs   import sort_logs
from .hes2raman   import hes2raman
from .get_data    import get_data


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
