import help as h
import numpy as np

def opt2hes(optfile, logfile):
    """
    This function changes the coordinates in input files that have not
    yet been run, to reduce optimization runtimes.

    Parameters
    ----------
    optfile: string
        This should be a string that points to the input file of an
        already run optimization file. (FULL DIRECTORY STRING REQUIRED)
    logfile: string
        This should be a string that points to the log file of an
        already run optimization file. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    This function returns nothing.

    Example
    -------
    >>> import opt2hes as oh
    >>>
    >>> #Note the './' directory is the one the BATCH script is in
    >>> logfile = './Optimization_Log_Folder/IBv6_NH3_CCSD-T_CC6_opt.log'
    >>> optfile = './IBv6_NH3_CCSD-T_CC6_opt.inp'
    >>>
    >>> oh.opt2hes(inpfile, logfile)
    >>>
    """
    #Define force line
    force     = ' $FORCE METHOD=FULLNUM NVIB=2 PROJCT=.TRUE. $END\n'
    if ('_B3LYP_' in optfile) or ('_MP2_' in optfile):
        force = ' $FORCE METHOD=SEMINUM NVIB=2 PROJCT=.TRUE. $END\n'
    if ('_CC5_' in optfile) or ('_CC6_' in optfile) or ('_PCseg-4_' in optfile):
        force = ' $FORCE METHOD=FULLNUM NVIB=2 PROJCT=.TRUE. $END\n'

    #Define Runtyps
    ropt = '=OPTIMIZE'
    rhes = '=HESSIAN'

    #Define file identifiers
    opt = '_opt'
    hes = '_hes'

    #Open, read in, and close log file
    f   = open(logfile, 'r')
    log = f.readlines()
    f.close()

    #Grabs optimized geometries tail index
    find = 'COORDINATES OF ALL ATOMS ARE'
    tail = len(log) - h.ctr_f(find, log[::-1]) - 1

    #Grabs optimized geometries header index
    find = '***** EQUILIBRIUM GEOMETRY LOCATED *****'
    head = h.ctr_f(find, log) + 4

    #Checks to make sure head and tail exist
    if (head is None) or (tail is None):
        print('LOL You Suck!')
        return

    #Assemble list of optimized geometry coordinates and get size
    coords = log[head : tail]
    n      = tail - head

    #Generate dictionary of atom coordinates
    atomdict = {}

    #Fill in atom dictionary
    for i in np.arange(0, n, 1):

        #Define key/value for atomdict
        key   = coords[i].split()[0] + '     ' + coords[i].split()[1] #ugly
        value = coords[i]

        #Fill dictionary
        atomdict[ key ] = value

    #Open, read in, and close input file
    f   = open(optfile, 'r')
    inp = f.readlines()
    f.close()

    #Replace OPTIMIZATION with HESSIAN
    i      = h.ctr_f(ropt, inp)
    inp[i] = inp[i].replace(ropt, rhes)

    #Insert force line into hessian input
    inp.insert(8, force)

    #Replace coordinates in file
    for key in atomdict:
        index = h.ctr_f(key, inp)
        inp[index] = atomdict[key]

    #Open, write, and close input file
    hesfile = optfile.replace(opt, hes)
    f       = open(hesfile, 'w')
    f.writelines(inp)
    f.close()

    return
