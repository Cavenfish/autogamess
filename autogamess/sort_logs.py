from .config import *

def sort_logs(projdir, logsdir):
    """
    This function sorts all the loose log files in the 'Logs' directory.

    Parameters
    ----------
    projdir: string
        A directory string (including the final `/`) that points to the
        project head directory.
    logsdir: string
        A directory string (including the final `/`) that points to the
        directory containing the log files.

    Returns
    ----------
    This function returns nothing

    Notes
    ----------
    For this function to work properly the project directory tree must be
    in the exact format that the 'new_project' fucntion spawned it in.

    Examples
    ----------
    >>>import autogamess as ag
    >>>
    >>>projdir = './Example/'
    >>>logsdir = './logs/'
    >>>
    >>>ag.sort_logs(projdir, logsdir)
    >>>
    """
    #Defining directory names
    sorteddir      = projdir + 'Logs/Sorted/'

    #Checks if sorteddir is real directory
    if not os.path.isdir(sorteddir):
        sorteddir = projdir

    #Defining extension names
    lgext    = '.log'

    for filename in os.listdir(logsdir):

        #Skips non-log files
        if lgext not in filename:
            continue

        #Gets molecule name, then puts string in directory format
        specie  = filename.split('_')[1]
        specie += '/'

        #Define the directory to put this particular file in
        move2 = sorteddir + specie

        #Checks if move2 directory exists, if not then makes it
        if not os.path.isdir(move2):
            os.makedirs(move2)

        #Define `before/after` of rename command to move file
        before = logsdir + filename
        after  = move2   + filename

        #Moves log to proper directory
        os.rename(before, after)


    return
