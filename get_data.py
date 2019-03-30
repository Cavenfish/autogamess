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
    """

    return data

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
        already run raman file. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    freq: list
        A list containing all the vibrational frequencies in string format
    time: string
        A string containing the calculation runtime
    cpu: string
        A string containing the cpu utilization
    """
    f=open(filename, 'r')
    log = f.readlines()
    f.close()

    end = h.ctr_f('...END OF NORMAL COORDINATE ANALYSIS...', log)

    if end != -1:
        time = log[end +2].split()[4]
        cpu  = log[end +2].split()[9]
    else:
        time = 'N/A'
        cpu  = 'N//A'

    freq = ','.join(h.ctr_f_allR('FREQUENCY', log)[1].split())

    return freq, (time, cpu)

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
