"""
This file houses the functions that grab data from log files.

Note, the optimization function only grabs raw data
"""
import numpy as np
import help as h
from scipy.spatial import distance

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
    data:
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
    equil = h.ctr_f(efind, log)

    #Grabs optimized geometries tail index
    hfind = 'INTERNUCLEAR DISTANCES (ANGS.)'
    lhead = len(log) - h.ctr_f(hfind, log[::-1]) + 3

    #Grabs optimized geometries header index
    tfind = '* ... LESS THAN  3.000'
    ltail = len(log) - h.ctr_f(tfind, log[::-1]) - 1

    #Get end of log file, for finding time and cpu
    e   = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end = h.ctr_f(e, log)

    #Checks to make sure head and tail exist
    if (lhead is -1) or (ltail is -1) or (equil is -1) or (end is -1):
        print("\n*****uh oh spaghettios*****\n")
        print("Either:" + tfind +
              "\n    or:" + hfind +
              "\n    or:" + efind +
              "\n    or:" + e +
              "\nIs not in " + filename)
        print("\n*****Ponder this, then return to me*****\n")
        return

    #Defines list of bond lengths
    lengths = log[lhead : ltail]

    #Makes smaller list to ctr_f through
    temp  = log[equil : lhead]

    #Finds start of full coordinate analysis
    s     = 'COORDINATES OF ALL ATOMS ARE (ANGS)'
    start = h.ctr_f(start, temp) + 3

    #Make matrix of atom coordinates
    matrix = {}
    for line in temp[start : -3]:
        matrix[line.split()[0]] = line.split()[2:4]

    #Make angles list
    angles = []
    for key in matrix:
        for key2 in matrix:
            if key2 is key:
                continue
            a1    = matrix[key ].astype(np.float)
            a2    = matrix[key2].astype(np.float)
            angle = h.angle_between(a1, a2)
            angles.append(key + '-' + key2 + ':' + angle)

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
    dhead = h.ctr_f('MODE FREQ(CM**-1)  SYMMETRY  RED. MASS  IR INTENS.', log)
    dtail = h.ctr_f('THERMOCHEMISTRY AT T=  298.15 K', log) - 1

    #Get end of log file, for finding time and cpu
    end   = h.ctr_f('EXECUTION OF GAMESS TERMINATED NORMALLY', log)

    #Checks is ctr_f fucntion actually found something
    if end != -1:
        time = log[end -2].split()[4]
        cpu  = log[end -2].split()[9]
    else:
        time = 'N/A'
        cpu  = 'N//A'

    #Make data list
    data = log [dhead:dtail]

    return data, (time, cpu)

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
    dhead = h.ctr_f('MODE FREQ(CM**-1)  SYMMETRY  RED. MASS  IR INTENS.', log)
    dtail = h.ctr_f('THERMOCHEMISTRY AT T=  298.15 K', log) - 1

    #Get end of log file, for finding time and cpu
    end   = h.ctr_f('EXECUTION OF GAMESS TERMINATED NORMALLY', log)

    #Checks is ctr_f fucntion actually found something
    if end != -1:
        time = log[end -2].split()[4]
        cpu  = log[end -2].split()[9]
    else:
        time = 'N/A'
        cpu  = 'N//A'

    #Make data list
    data = log [dhead:dtail]

    return data, (time, cpu)
