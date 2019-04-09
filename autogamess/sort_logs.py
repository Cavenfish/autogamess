
def sort_logs(projdir):
    """
    This function sorts all the loose log files in the 'Logs' directory.

    Parameters
    ----------
    projdir: string
        A directory string (including the final `/`) that points to the
        project head directory.

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
    >>>sort_logs(projdir)
    >>>
    """
    #Defining directory names
    sorteddir      = projdir + 'Logs/Sorted/'
    logsdir        = projdir + 'Logs/'

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

        #Define `before/after` of rename command to move file
        before = logsdir + filename
        after  = move2   + filename

        #Moves log to proper directory
        os.rename(before, after)


    return
