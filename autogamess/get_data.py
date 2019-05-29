"""
This file houses the functions that grab data from log files.

Note, the optimization function only grabs raw data
"""
from scipy.spatial import distance
from .config import *

#---------------------------------------------------------------------
#                        OPTIMIZATION FUNCTION
#---------------------------------------------------------------------

def optimization(filename):
    """
    This function produces the bond angle and length from calculated geometries.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of an
        already run optimization file. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    lenths: list
        A list where each element is a length between two atoms.
        All elements are strings with the following format:
            atom1-atom2:bond_length
    angles: list
        A list where each element is an angle between two atoms.
        Angles are in radians,( float/decimal numbers)
        All elements are strings with the following format:
            atom1-atom2:bond_angle
    time: string
        A string containing the calculation runtime
    cpu: string
        A string containing the cpu utilization
    """
    #Open to read Log file, then close to protect file
    f=open(filename, 'r')
    log = f.readlines()
    f.close()

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
    check_if_exists(equil, ctr_f(hfind, log[::-1]), end)

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

    #Make angles list
    lengths = []
    angles  = []
    for key in matrix:
        for key2 in matrix:
            a1     = make_xzy(matrix[key] )
            a2     = make_xzy(matrix[key2])
            angle  = angle_between(a1, a2)
            length = distance.euclidean(a1, a2)
            angles.append(key + '-' + key2 + ':' + str(angle) + '\n')
            lengths.append(key + '-' + key2 + ':' + str(length) + '\n')

    #Checks is ctr_f fucntion actually found something
    if end != -1:
        time = log[end -2].split()[4]
        cpu  = log[end -2].split()[9]
    else:
        time = 'N/A'
        cpu  = 'N//A'

    return lengths, angles, (time, cpu)

#---------------------------------------------------------------------
#                           HESSIAN FUNCTION
#---------------------------------------------------------------------

def hessian(filename):
    """
    This function grabs frequency data from a gamess hessian log file.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of an
        already run hessian file. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    data: list
        A list containing various strings with all the vibrational frequency,
        and IR intensities data. When the list is printed or writen to a file
        it will be tabular.
    time: string
        A string containing the calculation runtime
    cpu: string
        A string containing the cpu utilization
    """
    #Open to read Log file, then close to protect file
    f=open(filename, 'r')
    log = f.readlines()
    f.close()

    #Get head and tail of data
    hfind = 'MODE FREQ(CM**-1)  SYMMETRY  RED. MASS  IR INTENS.'
    dhead = ctr_f(hfind, log)
    tfind = 'THERMOCHEMISTRY AT T=  298.15 K'
    dtail = ctr_f(tfind, log) - 1

    #Get end of log file, for finding time and cpu
    efind = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end   = ctr_f(efind, log)

    #Checks is ctr_f fucntion actually found something
    check_if_exists(dhead, ctr_f(tfind, log), end)

    #Gets time and CPU utilization
    time = log[end -2].split()[4]
    cpu  = log[end -2].split()[9]

    #Make data list
    data = log [dhead:dtail]

    return data, time, cpu

#---------------------------------------------------------------------
#                           RAMAN FUNCTION
#---------------------------------------------------------------------

def raman(filename):
    """
    This function grabs frequency, IR, and raman data from a gamess raman
    log file.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of an
        already run raman file. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    data: list
        A list containing various strings with all the vibrational frequency,
        IR intensities, and raman activities data. When the list is printed
        or writen to a file it will be tabular.
    time: string
        A string containing the calculation runtime
    cpu: string
        A string containing the cpu utilization
    """
    #Open to read Log file, then close to protect file
    f=open(filename, 'r')
    log = f.readlines()
    f.close()

    #Get head and tail of data
    hfind = 'MODE FREQ(CM**-1)  SYMMETRY  RED. MASS  IR INTENS.'
    dhead = ctr_f(hfind, log)
    tfind = 'THERMOCHEMISTRY AT T=  298.15 K'
    dtail = ctr_f(tfind, log) - 1

    #Get end of log file, for finding time and cpu
    efind = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end   = ctr_f(efind, log)

    #Checks is ctr_f fucntion actually found something
    check_if_exists(dhead, ctr_f(tfind, log), end)

    #Gets time and CPU utilization
    time = log[end -2].split()[4]
    cpu  = log[end -2].split()[9]

    #Make data list
    data = log [dhead:dtail]

    return data, time, cpu
