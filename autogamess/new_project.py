from .config import *

def new_project(maindir, txtfile, title='Project_Name/'):
    """
    This function creates a new directory tree for a GAMESS project, also makes
    a couple of text files for use with other functions.

    Parameters
    ----------
    maindir: string
        A directory string (including the final `/`) that points to the
        directory that the project tree will be spawned in.
    txtfile: string
        A directory string (including the final `.txt`) that points to the
        text file containing project information. Read module documentation
        for txt file format.
    title: string
        A directory string (including the final `/`) that will be used as
        the head of project directory tree.

    Returns
    ----------
    This function returns nothing

    Notes
    ----------
    The format of the spawned directory tree is as follows:

                                    maindir
                                       |
                                     title
                        -------------------------------------
                        |        |        |        |        |
                      Codes    Inps     Logs  Batch_Files  Spreadsheets
                        |        |        |                     |
                  ---------    Block    -----------      1 file per specie
                  |       |             |    |    |
            Text_Files  Scripts      Fail   Pass  Sorted
                                      |      |        |
                                   -------  Block   1 directory per specie
                                   |     |
                             Unsolved   Solved


    Sections in directory tree labled 'Block' are directory trees with the
    following format:
                      1 directory per run type
                                  |
                      1 directory per specie

    Examples
    ----------
    >>> import new_project as np
    >>> txtfile = './somefile.txt'
    >>> np.new_project('./', txtfile, title='Example/')
    >>>
    """

    #Defining directory names
    scripts  = maindir + title + 'Codes/Scripts/'
    txtfiles = maindir + title + 'Codes/Text_Files/'
    unsolved = maindir + title + 'Logs/Fail/Unsolved/'
    solved   = maindir + title + 'Logs/Fail/Solved/'
    bats     = maindir + title + 'Batch_Files/'
    xldir    = maindir + title + 'Spreadsheets/'
    inputs   = maindir + title + 'Inps/'
    goodlogs = maindir + title + 'Logs/Pass/'
    sorrted  = maindir + title + 'Logs/Sorted/'

    #Define random commands
    fin      = '\nBREAK\n'
    engine   = 'xlsxwriter'
    xlsx     = '.xlsx'

    #Define DataFrame
    df = pd.DataFrame({})

    #Make directories
    os.makedirs(scripts)
    os.makedirs(txtfiles)
    os.makedirs(unsolved)
    os.makedirs(solved)
    os.makedirs(bats)
    os.makedirs(xldir)

    #Read in txt contents and generate species and runtyps lists
    f       = open(txtfile, 'r')
    info    = f.readlines()
    f.close()
    a       = ctr_f('Species', info)   + 1
    b       = ctr_f('-'      , info)
    species = [i.replace('\n', '/') for i in info[a:b] ]
    a       = ctr_f('Run Types', info) + 1
    b       = ctr_f('--'       , info)
    runtyps = [i.replace('\n', '/') for i in info[a:b] ]

    #Make Block directory trees
    for runtyp in runtyps:
        for specie in species:
            os.makedirs(inputs+runtyp+specie)
            os.makedirs(goodlogs+runtyp+specie)

    #More directory making and Excell workbook and sheet making
    for specie in species:
        os.makedirs(sorrted+specie)

        #Define header for Spreadsheets
        header = ['Project Name : ' +  title.replace('/', ''),
                  'Molecule Name: ' + specie.replace('/', '')]

        #Define Excell filename
        xlfilename = xldir + specie.replace('/', xlsx)

        #Initialize writer
        writer = pd.ExcelWriter(xlfilename, engine=engine)

        #Make Sheets and put headers on them all
        for runtyp in runtyps:

            #Define sheet name and make it
            sheet     = runtyp.replace('/', '')
            df.to_excel(writer, startrow=4, startcol=0, sheet_name=sheet)
            worksheet = writer.sheets[sheet]

            #Write header
            for line in header:
                i = header.index(line)
                worksheet.write(i, 0, line)

        #Save Excell file
        writer.save()


    #Move txtfile into Text_Files directory
    old = txtfile
    new = txtfiles + txtfile.split('/')[-1]
    os.rename(old, new)

    #Write text file
    f=open(txtfiles+'BuilderData.txt', 'w')
    f.writelines(runtyps)
    f.write(fin)
    f.writelines(species)
    f.write(fin)
    f.close()


    return
