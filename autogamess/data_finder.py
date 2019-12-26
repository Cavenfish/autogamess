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
        i    = ctr_f_last('TOTAL WALL CLOCK TIME', log)
        time = log[i].split()[4]
        cpu  = log[i].split()[9]
    else:
        time = 'Error'
        cpu  = 'Error'

    return [cpu, time]


#---------------------------------------------------------------------
#                        OPTIMIZATION FUNCTION
#---------------------------------------------------------------------

def optimization(filename):
    """
    This function collects data from GAMESS(us) optimization log files.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of a
        GAMESS(us) optimization calculation. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    The return is a list, where item 0 is `lengths` and item 1 is `angles`

    lengths: dictionary
        This is a dictionary where the key is in the format `atom1-atom2`
        and the value is a string with the bond length in angstrums.
    angles: dictionary
        This is a dictionary where the key is in the format `atom1-atom2-atom3`
        where atom2 is the central atom and the value is a string with the
        bond angle between the three atoms in radians.

    Notes
    -------
    This function is primarily intended for interal use by AutoGAMESS.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> filename = './AGv0-0-6_NH3_CCSD-T_CC6_opt.log'
    >>>
    >>> ag.data_finder.optimization(filename)
    >>>
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
            if a1 == a2:
                continue
            length = distance.euclidean(a1, a2)
            lengths[key + '-' + key2 + ' Bond Length'] = str(length)
            for key3 in matrix:
                a3 = make_xzy(matrix[key3])
                if (a3 == a2) or (a3 == a1):
                    continue
                angle  = find_bond_angle(a1, a2, a3) * (360.0 / (2.0 * np.pi))
                label  = key2 + '-' + key + '-' + key3 + ' Bond Angle'
                angles[label]  = str(angle)

    return [lengths, angles]

#---------------------------------------------------------------------
#                           HESSIAN FUNCTION
#---------------------------------------------------------------------

def hessian(filename):
    """
    This function collects data from GAMESS(us) Hessian log files.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of a
        GAMESS(us) hessian calculation. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    The return is a list, where item 0 is `freq` and item 1 is `infr`

    freq: dictionary
        This is a dictionary where the key is the symmetry and the value is
        the vibrational frequency.
    infr: dictionary
        This is a dictionary where the key is the symmetry and the value is
        infrared intensity.

    Notes
    -------
    This function is primarily intended for interal use by AutoGAMESS.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> filename = './AGv0-0-6_NH3_CCSD-T_CC6_hes.log'
    >>>
    >>> ag.data_finder.hessian(filename)
    >>>
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
    This function collects data from GAMESS(us) raman log files.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of a
        GAMESS(us) raman calculation. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    ram: dictionary
        This is a dictionary where the key is the symmetry and the
        value is the raman activity.

    Notes
    -------
    This function is primarily intended for interal use by AutoGAMESS.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> filename = './AGv0-0-6_NH3_CCSD-T_CC6_raman.log'
    >>>
    >>> ag.data_finder.raman(filename)
    >>>
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

    ram   = ctr_f_all('RAMAN ACTIVITY:', log)
    sym  = ctr_f_all('SYMMETRY:',     log)

    temp1 = flatten([x.split() for x in ram])
    temp2 = flatten([x.split() for x in sym])

    while 'I' in temp1:
        i           = temp1.index('I')
        temp1[i-1] *= -1
        del(temp1[i])

    ram = {}
    for a,b in zip(temp1[modes:],temp2[modes:]):
        if b not in ram:
            ram[b] = [a]
        else:
            ram[b] += [a]

    return ram

#---------------------------------------------------------------------
#                           VSCF FUNCTION
#---------------------------------------------------------------------

def vscf(filename):
    """
    This function collects data from GAMESS(us) VSCF log files.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of a
        GAMESS(us) VSCF calculation. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    The return is a list, where item 0 is `freq` and item 1 is `infr`

    freq: dictionary
        This is a dictionary where the key is the symmetry and the value is
        the vibrational frequency.
    ir: dictionary
        This is a dictionary where the key is the symmetry and the value is
        infrared intensity.

    Notes
    -------
    This function is primarily intended for interal use by AutoGAMESS.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> filename = './AGv0-0-6_NH3_CCSD-T_CC6_vscf.log'
    >>>
    >>> ag.data_finder.vscf(filename)
    >>>
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
    hfind1 = 'FREQUENCY, CM-1  INTENSITY, KM/MOL    EXCITATION'
    dhead1 = ctr_f(hfind1, log) + 1
    hfind2 = 'MODE   FREQUENCY, CM-1  INTENSITY, KM/MOL'
    dhead2 = ctr_f(hfind2, log) + 1
    tfind  = '......FINISHED VIBRATIONAL SCF......'
    dtail  = ctr_f(tfind, log)

    if dhead1 != 0:
        #Make Frequency and Infrared Intensity dictionaries
        freq = {}
        ir   = {}
        for line in log[dhead1:dtail]:
            a = line.split()[2] + ' ' + line.split()[3] + ' ' + line.split()[4]
            b = line.split()[0]
            c = line.split()[1]
            freq[a] = b
            ir[a]   = c

    if dhead2 != 0:
        #Make Frequency and Infrared Intensity dictionaries
        freq = {}
        ir   = {}
        for line in log[dhead2:dtail]:
            a = line.split()[0]
            b = line.split()[1]
            c = line.split()[2]
            freq[a] = b
            ir[a]   = c

    return [freq, ir]


#---------------------------------------------------------------------
#                     COMPOSITE METHOD FUNCTION
#---------------------------------------------------------------------

def composite(filename):
    """
    """
    #Read in contents of log file
    log = read_file(filename)

    #Get end of log file, for confirming successful run
    efind = 'EXECUTION OF GAMESS TERMINATED NORMALLY'
    end   = ctr_f(efind, log)

    #Checks is ctr_f fucntion actually found something
    if check_if_exists(filename, end):
        return (0,0,0)

    #Get index of lines with data from log file
    i0k   = ctr_f('HEATS OF FORMATION   (0K):', log)
    i298k = ctr_f('HEATS OF FORMATION (298K):', log)

    #Get data from log file
    hf0k   =   log[i0k].split(':')[1].strip(' ').split(' ')[0]
    hf298k = log[i298k].split(':')[1].strip(' ').split(' ')[0]

    return [hf0k, hf298k]
