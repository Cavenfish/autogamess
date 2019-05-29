from .config        import *
from .input_builder import input_builder

def new_project(maindir, csvfile, initial_coords_dict, ebasis_dir,
                title='Project_Name/'):
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
    unsolved = maindir + title + 'Logs/Fail/Unsolved/'
    solved   = maindir + title + 'Logs/Fail/Solved/'
    xldir    = maindir + title + 'Spreadsheets/'
    inputs   = maindir + title + 'Inps/'
    goodlogs = maindir + title + 'Logs/Pass/'
    sorrted  = maindir + title + 'Logs/Sorted/'

    #Define random commands
    fin      = '\nBREAK\n'
    engine   = 'xlsxwriter'
    xlsx     = '.xlsx'

    #Make directories
    os.makedirs(unsolved)
    os.makedirs(solved)
    os.makedirs(xldir)

    #Read in csv file
    df = pd.read_csv(csvfile)

    #Make lists of species, run-types, basis_sets, theories
    runtyps    = [str(x) + '/' for x in list(df['Run Types'].dropna())]
    species    = [str(x) + '/' for x in list(df['Species'].dropna())]
    theories   = list(df['Theory'].dropna())
    basis_sets = list(df['Basis Sets'].dropna()) + list(
                 df['External Basis Sets'].dropna())

    #Make Block directory trees
    for runtyp in runtyps:
        for specie in species:
            os.makedirs(inputs+runtyp+specie)
            os.makedirs(goodlogs+runtyp+specie)

    #Make data for Spreadsheets
    theo = []
    for theory in theories:
        temp    = [theory]*len(basis_sets)
        theo   += temp + ['\n', '\n','\n']

    bs = (basis_sets + ['\n', '\n','\n']) *len(theories)

    #Make dataframe with basis sets names only
    data = {'Theory': theo, 'Basis Set': bs}
    df2 = pd.DataFrame(data=data)

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
            df2.to_excel(writer, startrow=4, startcol=0, sheet_name=sheet)
            worksheet = writer.sheets[sheet]

            #Write Header
            for line in header:
                i = header.index(line)
                worksheet.write(i, 0, line)

        #Save Excell file
        writer.save()


    #Run Input Builder function
    save_dir = maindir + 'inputs/'
    input_builder(csvfile, initial_coords_dict, ebasis_dir,
                  save_dir, title.replace('/', '\n'))


    return
