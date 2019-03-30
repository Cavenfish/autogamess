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
    freq: list
        A list containing all the vibrational frequencies in string format
    ir: list
        A list containing all the IR instensities in string format
    raman: list
        A list containing all the raman activites in string format
    time: string
        A string containing the calculation runtime
    cpu: string
        A string containing the cpu utilization
    """
    f=open(filename, 'r')
    log = f.readlines()
    f.close()

    end = h.ctr_f('... DONE WITH NORMAL COORDINATE ANALYSIS ...', log)

    if end != -1:
        time = log[end +2].split()[4]
        cpu  = log[end +2].split()[9]
    else:
        time = 'N/A'
        cpu  = 'N//A'

    freq  = ','.join(h.ctr_f_allR('FREQUENCY',      log)[1].split())
    ir    = ','.join(h.ctr_f_allR('IR INTENSITY',   log)[1].split())
    raman = ','.join(h.ctr_f_allR('RAMAN ACTIVITY', log)[1].split())

    return (freq, ir, raman), (time, cpu)
