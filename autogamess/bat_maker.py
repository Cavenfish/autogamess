from .config import *

def bat_maker(projdir, ncpus=1, ppn=0):
    """
    This function makes batch files that calls the 'rungms' file on each
    input file.

    Parameters
    ----------
    projdir: string
        A directory string (including the final `/`) that points to the
        project head directory.
    ncpus: int
        The number of compute processes requested for jobs that will be ran
        with batch file. Note that all files will run under this amount.
        Default vaule is 1.
    ppn: int
        The number of compute processes per node. Note that all files will
        run under this amount. Default vaule is 0.

    Returns
    --------
    No returned value unless an error is produced, then standard error message
    will be printed out.

    Notes
    -----


    """
    #Defining directory names
    bats           = projdir + 'Batch_Files/'
    inpdir         = projdir + 'Inps/'
    logdir         = projdir + 'Logs/'
    gamessdir      = '../../../'

    #Define error message
    stderr   = 'ERROR RUNNING BATCH MAKER, GAMESS NOT FOUND'

    #Defining extension names
    ipext    = '.inp'
    lgext    = '.log'
    baext    = '.bat'
    exe      = '.exe'

    #Define windows cmd commands and some extra stuff
    rungms   = 'call rungms'
    ping     = 'PING -n 10 127.0.0.1 > NUL'
    sb       = ' '  #Just a blank space (sb = spacebar)
    nl       = '\n'

    #Define GAMESS executable file name header
    ghead    = 'gamess.'

    #Define dictionary that knows


    #Get GAMESS version number
    for filename in os.listdir(gamessdir):
        if (ghead in filename) and (exe in filename):
            version = filename.split('.')[1]
            break
        else:
            return sys.exit(stderr)


    #Writes .bat file
    for folder in os.lisdir(inpdir):

        #Defines name of file as string, then opens .bat file to write in
        batname = bats + folder + baext
        f       = open(batname, 'w')

        #Make the folder name into directory style string
        fdir = inpdir + folder + '/'

        for folder2 in os.listdir(fdir):

            #Make 2nd folder name into directory style string
            typdir = fdir + folder2 + '/'

            #Write command to run input files into batch file
            f.write(rungms + sb + typdir + filename + sb + version + sb +
                    ncpus + sb + ppn + logdir +
                    filename.replace(ipext, logext) + nl + ping + nl + nl)

        #Write command to run post GAMESS python script
        #f.write()

        #Close file
        f.close()


    return
