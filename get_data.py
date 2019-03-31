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

    #Grabs optimized geometries tail index
    tfind = 'COORDINATES OF ALL ATOMS ARE'
    dtail = len(log) - h.ctr_f(tfind, log[::-1]) - 1

    #Grabs optimized geometries header index
    hfind = '***** EQUILIBRIUM GEOMETRY LOCATED *****'
    dhead = h.ctr_f(hfind, log) + 4

    #Checks to make sure head and tail exist
    if (dhead is -1) or (dtail is -1):
        print("\n*****uh oh spaghettios*****\n")
        print("Either:" + tfind + "\n    or:" + hfind +
              "\nIs not in " + logfile)
        print("\n*****Ponder this, then return to me*****\n")
        return



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
