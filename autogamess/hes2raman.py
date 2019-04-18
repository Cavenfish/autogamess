from autogamess import ctr_f

def hes2raman(hesfile, datfile):
    """
    This function changes the coordinates in input files that have not
    yet been run, to reduce optimization runtimes.

    Parameters
    ----------
    hesfile: string
        This should be a string that points to the input file of an
        already run optimization file. (FULL DIRECTORY STRING REQUIRED)
    datfile: string
        This should be a string that points to the DAT file of an
        already run optimization file. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    This function returns nothing.

    Example
    -------
    >>> import hes2raman as hr
    >>>
    >>> #Note the './' directory is the one the BATCH script is in
    >>> datfile = '../restart/IBv6_NH3_CCSD-T_CC6_hes.dat'
    >>> hesfile = './IBv6_NH3_CCSD-T_CC6_hes.inp'
    >>>
    >>> hr.hes2raman(hesfile, datfile)
    >>>
    """
    #Define Runtyps
    rhes   = '=HESSIAN'
    rraman = '=RAMAN'

    #Define grap list indexes
    s = ' $GRAD  \n'
    e = '----- HESSIAN MATRIX AFTER PROJECTION -----\n'

    #Define file identifiers
    hes   = '_hes'
    raman = '_raman'

    #Define raman file
    ramanfile = hesfile.replace(hes, raman)

    #Open, Read then close input file
    f   = open(hesfile, 'r')
    inp = f.readlines()
    f.close()

    #Open, Read then close DAT file
    f    = open(datfile, 'r')
    grab = f.readlines()
    f.close()

    if (s not in grab) or (e not in grab):
        print(error_head)
        print("Either:" + s + "\n    or:" + e + "\nIs not in " + datfile)
        print(error_tail)
        return

    #Define start and end indexes
    start = grab.index(s)
    end   = grab.index(e)

    #Replace HESSIAN with RAMAN
    i      = ctr_f(rhes, inp)
    inp[i] = inp[i].replace(rhes, rraman)

    #Open, Write then close raman file
    f = open(ramanfile, 'w')
    f.writelines(inp)
    f.writelines(grab[start:end])
    f.close()

    return
