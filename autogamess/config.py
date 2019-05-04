import os
import sys
import numpy  as np
import pandas as pd


error_head = "\n*****uh oh spaghettios*****\n"
error_tail = "\n*****Ponder this, then return to me*****\n"

def check_if_exists(*args):
    for arg in args:
        if arg is -1:
            print(error_head)
            print('Something went wrong, check your log file')
            print(error_tail)
            sys.exit()
    return

def check_if_in(*args, look_here):
    for arg in args:
        if arg not in look_here:
            print(error_head)
            print(arg + '\n Not Found')
            print(error_tail)
            sys.exit()
    return

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
