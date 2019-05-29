import os
import sys
import numpy  as np
import pandas as pd

#Error messages
error_head   = "\n*****uh oh spaghettios*****\n"
error_tail   = "\n*****Ponder this, then return to me*****\n"

#Basic input file parameters
basic_params = (' $CONTRL SCFTYP=RHF MULT=1 NPRINT=0 COORD=UNIQUE\n',
                ' RUNTYP=OPTIMIZE ICUT=12 ITOL=25 theory\n',
                ' MAXIT=200 QMTTOL=1E-7 ICHARG=0 ISPHER=1 $END\n',
                ' $SYSTEM MWORDS=800 MEMDDI=800 $END\n',
                ' $STATPT OPTTOL=1E-6 NSTEP=200 $END\n',
                ' $SCF DIRSCF=.TRUE. FDIFF=.FALSE. CONV=1d-7 $END\n',
                ' $DFT JANS=2 $END\n',
                ' $BASIS GBASIS=basis $END\n',
                ' $DATA\n')

#Dictionary for theory levels and their input parameters
theory_dict = {'B3LYP': 'DFTTYP=B3LYP',
               'MP2': 'MPLEVL=2',
               'CCSD-T': 'CCTYP=CCSD(T)'}


#Basic functions used throughout code-----------------------------------
def check_if_exists(*args):
    for arg in args:
        if arg is -1:
            msg = "Something went wrong, check your log file"
            sys.exit(error_head + msg + error_tail)
    return

def check_if_in(*args, look_here):
    for arg in args:
        if arg not in look_here:
            msg = arg + "\n Not Found"
            sys.exit(error_head + msg + error_tail)
    return

def ctr_f(find_this, look_here):
    for line in look_here:
        if find_this in line:
            return look_here.index(line)
    return -1

def ctr_f_allR(find_this, look_here):
    r = []
    for line in look_here:
        if "TERMINATED -ABNORMALLY-" in line:
            r.append("N/A")
            r.append("N/A")
        if find_this in line:
            r.append(line.split(':')[1])

    return r

def angle_between(v1, v2):
    v1hat = v1 / np.linalg.norm(v1)
    v2hat = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1hat, v2hat), -1.0, 1.0))

def make_xzy(xyzlist):
    r = (float(xyzlist[0]),
         float(xyzlist[1]),
         float(xyzlist[2]))
    return r
