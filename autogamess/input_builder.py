from .config import *
import pkg_resources
from .molecule_dictionary import molecule_dictionary

def input_builder(inputfile, save_dir, initial_coords_dict=None,
                  proj_title=' Your Title Goes Here\n'):
    """
    This function builds optimization input files.

    Parameters
    ----------


    Returns
    ----------
    This function returns nothing

    Notes
    ----------
    This function uses the EMSL Basis Set Exchange module to import
    external basis sets[1]. This function also uses the Periodic_Elements
    package by VaasuDevanS [2].

    [1] https://github.com/MolSSI-BSE/basis_set_exchange
    [2] https://github.com/VaasuDevanS/Periodic_Elements


    Examples
    ----------
    """
    #Variable Declrations
    _       = '_'
    version = (' AutoGAMESS Version ' +
                str(pkg_resources.require("autogamess")[0].version) )
    ibv     = 'AGv' + version.split(' ')[-1].replace('.', '-')
    opt     = '_opt.inp'

    #Checks if initial_coords_dict is given
    if initial_coords_dict is None:
        initial_coords_dict = molecule_dictionary

    #Read in input file
    df = pd.read_csv(inputfile)

    #Get list of species/theories/basis sets
    species     = list(df['Species'].dropna())
    theories    = list(df['Theory'].dropna())
    basis_sets  = list(df['Basis Sets'].dropna())
    ebasis_sets = list(df['External Basis Sets'].dropna())

    #Make list of file names
    files = []
    for specie in species:
        for theorie in theories:
            for ebasis in ebasis_sets:
                files.append( ibv+ _ + specie.strip('\n') + _ +
                              theorie.strip('\n') + _ +
                              ebasis.strip('\n') + opt )
            for basis in basis_sets:
                files.append( ibv+ _ + specie.strip('\n') + _ +
                              theorie.strip('\n') + _ +
                              basis.strip('\n') + opt )

    #Make input files for GAMESS(us)
    for filename in files:
        #Open file, write preamble
        f = open(save_dir + filename, 'w')
        f.write('!'+ version +'\n')
        f.write('!  by Brian C. Ferrari \n')
        f.write('!\n')

        #Get index of 'theory' to replace with proper command
        i               = ctr_f('theory', basic_params)

        #Get proper theory input style from dictionary
        theo            = theory_dict[filename.split(_)[2]]

        #Get list version of tuple basic parameters
        #(its a tuple to protect it from changes)
        params          = list(basic_params)

        #Replace 'theory' with proper input parameter
        params[i]       = basic_params[i].replace('theory', theo)

        #Fill in basis parameter for GAMESS(us) internal basis sets
        if filename.split(_)[3] in basis_sets:
            i               = ctr_f('=basis', basic_params)
            bset            = filename.split(_)[3]
            params[i]       = basic_params[i].replace('basis', bset)
        #If not internal delete basis line from input file
        else:
            i               = ctr_f('=basis', basic_params)
            del params[i]

        #Write parameters, and project title
        f.writelines(params)
        f.write(proj_title)

        #Get initial coordinates from initial_coords_dict
        coords = initial_coords_dict[filename.split(_)[1]]

        #Useing EMSL put in external basis sets
        if filename.split(_)[3] in ebasis_sets:
            basis_name = filename.split(_)[3]
            molecule   = filename.split(_)[1]
            atoms      = [x for x in molecule if not x.isdigit()]


    return
