"""
This is the configuration file for AutoGAMESS.

Houses various variables/functions used commonly by AutoGAMESS.
"""
import os
import sys
import numpy  as np
import pandas as pd
import basis_set_exchange as bse

#Error messages
error_head   = "\n*****uh oh spaghettios*****\n"
error_tail   = "\n*****Ponder this, then return to me*****\n"

#Basic input file parameters for optimization calculation
basic_params = (' $CONTRL SCFTYP=RHF MULT=1 NPRINT=0 COORD=UNIQUE\n',
                ' RUNTYP=OPTIMIZE ICUT=12 ITOL=25 theory\n',
                ' MAXIT=200 QMTTOL=1E-7 ICHARG=0 ISPHER=1 $END\n',
                ' $SYSTEM MWORDS=800 MEMDDI=800 $END\n',
                ' $STATPT OPTTOL=1E-6 NSTEP=200 $END\n',
                ' $SCF DIRSCF=.TRUE. FDIFF=.FALSE. CONV=1d-7 $END\n',
                ' $DFT JANS=2 $END\n',
                ' $BASIS GBASIS=basis $END\n',
                ' $DATA\n')

#Basic input file parameters for composite method calculation
comp_basic_params = (' $CONTRL SCFTYP=RHF MULT=1 NPRINT=0 COORD=UNIQUE\n',
                     ' RUNTYP=COMP ICUT=12 ITOL=25 MAXIT=200\n',
                     ' QMTTOL=1E-7 ICHARG=0 ISPHER=1 $END\n',
                     ' $COMP theory $END\n',
                     ' $SYSTEM MWORDS=800 MEMDDI=800 $END\n',
                     ' $STATPT OPTTOL=1E-6 NSTEP=200 $END\n',
                     ' $SCF DIRSCF=.TRUE. FDIFF=.FALSE. CONV=1d-7 $END\n',
                     ' $DATA\n')

#Basic functions used throughout code-----------------------------------
def check_if_exists(filename, *args):
    for arg in args:
        if arg is -1:
            msg = "Something went wrong, check your log file\n" + filename
            print(error_head + msg + error_tail)
            return True
    return False

def check_if_in(filename, *args, look_here):
    for arg in args:
        if arg not in look_here:
            msg = arg + "\n Not Found in " + filename
            sys.exit(error_head + msg + error_tail)
    return

def ctr_f(find_this, look_here):
    for line in look_here:
        if find_this in line:
            return look_here.index(line)
    return -1

def ctr_f_all(find_this, look_here):
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

def find_bond_angle(o,i,j):
    v1 = np.array(i) - np.array(o)
    v2 = np.array(j) - np.array(o)
    return angle_between(v1,v2)

def make_xzy(xyzlist):
    r = (float(xyzlist[0]),
         float(xyzlist[1]),
         float(xyzlist[2]))
    return r

def flatten(array):
    r = []
    for i in array:
        r += i
    return r

def check_data_type(data):
    #Check if data is in CSV format
    if '.csv' in data:
        df = pd.read_csv(data)

    #Terminates function with error message if data format not acceptable
    elif type(data) is not type(pd.DataFrame()):
        print(error_head)
        print("Your data is not in CSV or Pandas DataFrame Format")
        print(error_tail)
        sys.exit()

    #If data already DataFrame format, changes its name to df
    else:
        df = data

    return df

def read_file(file):
    f=open(file, 'r')
    r=f.readlines()
    f.close()
    return r

def get_gamess_input(command, doc):
    i = ctr_f(command, doc)
    j = ctr_f(command, doc[i].split())
    return doc[i].split()[j].split('=')[1]

def gaussian(x, mu, sig, amp):
    return  np.exp(-(x-mu)**2 / (2.*sig**2)) * amp

def lorentzian(x, mu, sig, amp):
    return ( 1/( 1 + ( ((x-mu)**2)/(sig**2)) ) ) * amp

def scaling_factor_scott(theo, expt):
    top    = 0
    top2   = 0
    bottom = 0
    n      = range(len(theo))
    for i in n:
        top    += theo[i]*expt[i]
        bottom += theo[i]**2

    c  = round(top/bottom, 4)
    for i in n:
        top2 += (c*theo[i] - expt[i])**2

    rms = round(np.sqrt(top2/len(theo)), 2)

    return c, rms

def get_elements(molecule):
    atoms = []

    for i in range(len(molecule)):
        x = molecule[i]

        if x.isupper() and x.isalpha():
            if i != len(molecule)-1:
                y = molecule[i+1]

            if y.islower():
                atoms.append(x+y)
                y = ''
            else:
                atoms.append(x)

    return atoms

def conversion_factor(old, new):
    daa = 'Debye^2 angstrom^-2 amu^-1'
    kmm = 'km mol^-1'
    cmm = 'cm molecule^-1'

    if (old == daa) and (new == kmm):
        return 42.2547
    if (old == daa) and (new == cmm):
        return 7.017e-18
    if (old == kmm) and (new == daa):
        return (1/42.2547)
    if (old == kmm) and (new == cmm):
        return 1.661e-19
    if (old == cmm) and (new == daa):
        return (1/7.017e-18)
    if (old == cmm) and (new == kmm):
        return (1/1.661e-19)

    print(error_head)
    print("Your old or new units choice did not match any available options")
    print(error_tail)
    sys.exit()
