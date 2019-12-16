import pkg_resources
from .config        import *
from .input_builder import input_builder

def new_project(maindir, csvfile, initial_coords_dict=None,
                title='Project_Name/', make_inputs=False):
    """
    This function creates a new directory tree for a GAMESS project, also makes
    a couple of text files for use with other functions.

    Parameters
    ----------
    maindir: string
        A directory string (including the final `/`) that points to the
        directory that the project tree will be spawned in.
    csvfile: string
        A directory string (including the final `.csv`) that points to the
        text file containing project information. Read module documentation
        for csv file format.
    initial_coords_dict: dictionary [Optional]
        This should be a dictionary with the key being the specie and the
        value being a list that of its inital coordinates.
    title: string [Optional]
        A directory string (including the final `/`) that will be used as
        the head of project directory tree.
    make_inputs: boolean True/False [Optional]
        if True then new_project will call input_builder at the end.

    Notes 1
    ----------
    If the molecules you wish to build are not already defined in the
    general autogamess coordinate dictionary, then initial_coords_dict
    must be passed.

    To see the autogamess coordianate dictionary simply print out
    >>> ag.dictionaries.molecule_dictionary

    Returns
    ----------
    This function returns nothing

    Notes 2
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
    >>> import autogamess as ag
    >>>
    >>> csvfile = './input.csv'
    >>> maindir = './'
    >>> title   = 'Project Title/'
    >>>
    >>> ag.new_project(maindir, csvfile, title=title)
    >>>
    """
    #Spreadsheet header phrase
    version = (' AutoGAMESS Version ' +
                str(pkg_resources.require("autogamess")[0].version) )
    author  = '     by Brian C. Ferrari'

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
    try:
        os.makedirs(unsolved)
        os.makedirs(solved)
        os.makedirs(xldir)
    except:
        sys.exit("Project Directory or sub-directories already exist")

    #Read in csv file or Pandas DataFrame
    df = check_data_type(csvfile)

    #Make lists of species, run-types, basis_sets, theories
    runtyps    = [str(x) + '/' for x in list(df['Run Types'].dropna())]
    species    = [str(x) + '/' for x in list(df['Species'].dropna())]
    theories   = list(df['Theory'].dropna())
    cmethods   = list(df['Composite Methods'].dropna())
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
    df2  = pd.DataFrame(data=data)

    #Make data for Composite method Sheets
    data = {'Method': cmethods}
    df3  = pd.DataFrame(data=data)


    #More directory making and Excell workbook and sheet making
    for specie in species:
        os.makedirs(sorrted+specie)

        #Define header for Spreadsheets
        header = [version, author, '',
                  'Project Name : ' +  title.replace('/', ''),
                  'Molecule Name: ' + specie.replace('/', '')]

        #Define Excell filename
        xlfilename = xldir + specie.replace('/', xlsx)

        #Initialize writer
        writer = pd.ExcelWriter(xlfilename, engine=engine)

        #Make Sheets and put headers on them all
        for runtyp in runtyps:

            #Define sheet name and make it
            if runtyp == 'Composite/':
                sheet     = runtyp.replace('/', '')
                df3.to_excel(writer, startrow=6, startcol=0, sheet_name=sheet)
                worksheet = writer.sheets[sheet]
            else:
                sheet     = runtyp.replace('/', '')
                df2.to_excel(writer, startrow=6, startcol=0, sheet_name=sheet)
                worksheet = writer.sheets[sheet]

            #Write Header
            for line in header:
                i = header.index(line)
                worksheet.write(i, 0, line)

            #Write Units in header
            u  = 'Units:'
            bl = 'Bond Length (angstroms)'
            ba = 'Bond Angle (radians)'
            vf = 'Vibrational Frequency (cm^-1)'
            ii = 'Infrared Intensity (Debye^2 angstrom^-2 amu^-1)'
            ra = 'Raman Activity (angstrom^4 amu^-1)'
            hf = 'Heat of Formation (kcal mol^-1)'
            if runtyp == 'Optimization/':
                worksheet.write(3, 4, u)
                worksheet.write(3, 6, bl)
                worksheet.write(3, 9, ba)
            if runtyp == 'Hessian/':
                worksheet.write(3, 4, u)
                worksheet.write(3, 6, vf)
                worksheet.write(3, 9, ii)
            if runtyp == 'Raman/':
                worksheet.write(3, 4, u)
                worksheet.write(3, 6, ra)
            if runtyp == 'Composite/':
                worksheet.write(3, 4, u)
                worksheet.write(3, 6, hf)

        #Save Excell file
        writer.save()


    #Run Input Builder function
    if make_inputs is True:
        save_dir = inputs
        input_builder(csvfile, save_dir, initial_coords_dict,
                     proj_title = title.replace('/', '\n'))


    return
