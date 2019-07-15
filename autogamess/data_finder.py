"""
This file houses the functions that grab data from log files.

Note, the optimization function only grabs raw data
"""
from scipy.spatial import distance
from .config import *

def comp(filename):
    #Read in contents of log file
    log = read_file(filename)

    #Get end of log file, for finding time and cpu
    e   = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end = ctr_f(e, log)

    #Checks is ctr_f fucntion actually found something
    if end != -1:
        time = log[end -2].split()[4]
        cpu  = log[end -2].split()[9]
    else:
        time = 'Error'
        cpu  = 'Error'

    return [cpu, time]


#---------------------------------------------------------------------
#                        OPTIMIZATION FUNCTION
#---------------------------------------------------------------------

def optimization(filename):
    """

    """
    #Read in contents of log file
    log = read_file(filename)

    #Grabs 'Equil' phrase index
    efind = '***** EQUILIBRIUM GEOMETRY LOCATED *****'
    equil = ctr_f(efind, log)

    #Grabs optimized geometries tail index
    hfind = 'INTERNUCLEAR DISTANCES (ANGS.)'
    lhead = len(log) - ctr_f(hfind, log[::-1]) + 2

    #Get end of log file, for finding time and cpu
    e   = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end = ctr_f(e, log)

    #Checks to make sure head and tail exist
    if check_if_exists(filename, equil, ctr_f(hfind, log[::-1]), end):
        return (0,0,0)

    #Makes smaller list to ctr_f through
    temp  = log[equil : lhead]

    #Finds start of full coordinate analysis
    s     = 'COORDINATES OF ALL ATOMS ARE (ANGS)'
    start = ctr_f(s, temp) + 3

    #Make matrix of atom coordinates
    matrix = {}
    i      = 2
    for line in temp[start : len(temp)-4]:

        if line.split()[0] in matrix:
            matrix[str(i)+line.split()[0]] = line.split()[2:5]
            i += 1
        else:
            matrix[line.split()[0]] = line.split()[2:5]

    #Make dictionaries
    lengths = {}
    angles  = {}
    for key in matrix:
        for key2 in matrix:
            a1     = make_xzy(matrix[key] )
            a2     = make_xzy(matrix[key2])
            angle  = angle_between(a1, a2)
            length = distance.euclidean(a1, a2)
            angles[key + '-' + key2 + ' Bond Angle']  = str(angle)
            lengths[key + '-' + key2 + ' Bond Length'] = str(length)

    return [lengths, angles]

#---------------------------------------------------------------------
#                           HESSIAN FUNCTION
#---------------------------------------------------------------------

def hessian(filename):
    """

    """
    #Read in contents of log file
    log = read_file(filename)

    #Get end of log file, for finding time and cpu
    efind = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end   = ctr_f(efind, log)

    #Checks if ctr_f fucntion actually found something
    if check_if_exists(filename, end):
        return (0,0,0)

    #Find Modes to ignore
    mfind  = 'ARE TAKEN AS ROTATIONS AND TRANSLATIONS.'
    mindex = ctr_f(mfind, log)
    modes  = int(log[mindex].split()[3])

    freq = ctr_f_all('FREQUENCY:',    log)
    ir   = ctr_f_all('IR INTENSITY:', log)
    sym  = ctr_f_all('SYMMETRY:',     log)

    temp1 = flatten([x.split() for x in freq])
    temp2 = flatten([x.split() for x in sym])
    temp3 = flatten([x.split() for x in ir])

    while 'I' in temp1:
        i           = temp1.index('I')
        temp1[i-1] *= -1
        del(temp1[i])

    freq = {}
    for a,b in zip(temp1[modes:],temp2[modes:]):
        if b not in freq:
            freq[b] = [a]
        else:
            freq[b] += [a]

    infr = {}
    for a,b in zip(temp3[modes:],temp2[modes:]):
        if b not in infr:
            infr[b] = [a]
        else:
            infr[b] += [a]

    return [freq, infr]

#---------------------------------------------------------------------
#                           RAMAN FUNCTION
#---------------------------------------------------------------------

def raman(filename):
    """

    """
    #Read in contents of log file
    log = read_file(filename)

    #Get end of log file, for finding time and cpu
    efind = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end   = ctr_f(efind, log)

    #Checks is ctr_f fucntion actually found something
    if check_if_exists(filename, end):
        return (0,0,0)

    #Find Modes to ignore
    mfind  = 'ARE TAKEN AS ROTATIONS AND TRANSLATIONS.'
    mindex = ctr_f(mfind, log)
    modes  = int(log[mindex].split()[3])

    #Get head and tail of data
    hfind = 'MODE FREQ(CM**-1)  SYMMETRY  RED. MASS  IR INTENS.'
    dhead = ctr_f(hfind, log) + 1 + modes
    tfind = 'THERMOCHEMISTRY AT T=  298.15 K'
    dtail = ctr_f(tfind, log) - 2

    #Checks is ctr_f fucntion actually found something
    if check_if_exists(filename, ctr_f(hfind, log), ctr_f(tfind, log)):
        return (0,0,0)

    #Make data dictionary
    data = {}
    for line in log[dhead:dtail]:
        a = line.split()[5]
        b = line.split()[2]
        if b not in data:
            data[b] = [a]
        else:
            data[b] += [a]

    return data

#---------------------------------------------------------------------
#                           VSCF FUNCTION
#---------------------------------------------------------------------

def vscf(filename):
    """
    """
    #Read in contents of log file
    log = read_file(filename)

    #Get end of log file, for finding time and cpu
    efind = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end   = ctr_f(efind, log)

    #Checks is ctr_f fucntion actually found something
    if check_if_exists(filename, end):
        return (0,0,0)

    #Get head and tail of data
    hfind = 'FREQUENCY, CM-1  INTENSITY, KM/MOL    EXCITATION'
    dhead = ctr_f(hfind, log) + 1
    tfind = '......FINISHED VIBRATIONAL SCF......'
    dtail = ctr_f(tfind, log)

    #Make Frequency and Infrared Intensity dictionaries
    freq = {}
    ir   = {}
    for line in log[dhead:dtail]:
        a = line.split()[2] + ' ' + line.split()[3] + ' ' + line.split()[4]
        b = line.split()[0]
        c = line.split()[1]
        freq[a] = b
        ir[a]   = c

    return [freq, ir]
