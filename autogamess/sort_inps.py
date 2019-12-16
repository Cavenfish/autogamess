from .config import *

def sort_inps(projdir, inpsdir):
    """
    This function sorts all the loose log files in the 'Logs' directory.

    Parameters
    ----------
    projdir: string
        A directory string (including the final `/`) that points to the
        project head directory.
    inpsdir: string
        A directory string (including the final `/`) that points to the
        directory containing the input files.

    Returns
    ----------
    This function returns nothing

    Notes
    ----------
    For this function to work properly the project directory tree must be
    in the exact format that the 'new_project' fucntion spawned it in.

    Examples
    ----------
    >>>import sort_logs
    >>>projdir = './Example/'
    >>>inpdir  = './Inps/'
    >>>sort_inps(projdir, inpsdir)
    >>>
    """
    #Defining Shorthand to directory name dictionary
    typ_dict = {'opt'  : 'Optimization/',
                'hes'  : 'Hessian/',
                'raman': 'Raman/',
                'vscf' : 'VSCF/',
                'comp' : 'Composite/'}

    #Defining directory names
    dir      = projdir + 'Inps/'

    #Checks if Inps dir is real directory
    if not os.path.isdir(dir):
        dir = projdir

    #Defining extension names
    ipext    = '.inp'

    for filename in os.listdir(inpsdir):

        #Skips non-inp files
        if ipext not in filename:
            continue

        #Get file runtype, then puts string in directory format
        typ0 = filename.split('_')[-1].split('.')[0]
        if typ0[-1].isnumeric():
            typ0 = typ0[0:-1]
        typ  = typ_dict[typ0]

        #Gets molecule name, then puts string in directory format
        specie  = filename.split('_')[1]
        specie += '/'

        #Define the directory to put this particular file in
        move2 = dir + typ + specie

        #Checks if move2 directory exists, if not then makes it
        if not os.path.isdir(move2):
            os.makedirs(move2)

        #Define `before/after` of rename command to move file
        before = inpsdir + filename
        after  = move2   + filename

        #Moves log to proper directory
        os.rename(before, after)


    return
