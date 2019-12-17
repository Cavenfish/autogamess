from .config import *
import pkg_resources
from .dictionaries import *
import elements.elements as el

def input_builder(inputfile, save_dir, initial_coords_dict=None,
                  proj_title=' Your Title Goes Here\n'):
    """
    This function builds optimization input files.

    Parameters
    ----------
    inputfile: string
        This should be a full directory string that points to the input
        csv file.
    save_dir: string
        this should be a full directory string that points to the directory
        you wish to save the inputs in.
    initial_coords_dict: dictionary [Optional]
        This should be a dictionary with the key being the specie and the
        value being a list of the symmetry group and symmetry unique atom
        coordinates. Examples can be seen in the AutoGAMESS GitHub repository
        as well as by prinint out the default dictionary, see Notes section.
    proj_title: string [Optional]
        This should be a string ending with `\n`

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
    This function uses the EMSL Basis Set Exchange module to import
    external basis sets[1]. This function also uses the Periodic_Elements
    package by VaasuDevanS [2].

    [1] https://github.com/MolSSI-BSE/basis_set_exchange
    [2] https://github.com/VaasuDevanS/Periodic_Elements


    Examples
    ----------
    >>> import autogamess as ag
    >>>
    >>> csvfile = './input.csv'
    >>> savedir = './'
    >>> title   = 'Project\n'
    >>>
    >>> ag.input_builder(csvfile, savedir, proj_title=title)
    >>>
    """
    #Variable Declrations
    _       = '_'
    version = (' AutoGAMESS Version ' +
                str(pkg_resources.require("autogamess")[0].version) )
    ibv     = 'AGv' + version.split(' ')[-1].replace('.', '-')
    opt     = '_opt.inp'
    cmp     = '_comp.inp'
    numgrd  = 'NUMGRD=.T.'

    #Checks if initial_coords_dict is given
    if initial_coords_dict is None:
        initial_coords_dict = molecule_dictionary

    #Read in input file
    df = pd.read_csv(inputfile)

    #Get list of species/theories/basis sets
    species     = list(df['Species'].dropna())
    theories    = list(df['Theory'].dropna())
    cmethods    = list(df['Composite Methods'].dropna())
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
        for cmethod in cmethods:
            files.append( ibv+ _ + specie.strip('\n') + _ +
                          cmethod.strip('\n') + cmp )

    #Make input files for GAMESS(us)
    for filename in files:
        #Open file, write preamble
        f = open(save_dir + filename, 'w')
        f.write('!'+ version +'\n')
        f.write('!  by Brian C. Ferrari \n')
        f.write('!\n')

        #Composit method input building
        if cmp in filename:
            theo      = comp_dict[filename.split(_)[2]]
            i         = ctr_f('theory', comp_basic_params)
            params    = list(comp_basic_params)
            params[i] = comp_basic_params[i].replace('theory', theo)

            if 'G4MP2' in theo:
                params.insert(ctr_f('$COMP', params)+1,
                              ' $FORCE METHOD=SEMINUM $END\n')

            #Write parameters, and project title
            f.writelines(params)
            f.write(proj_title)

            #Get initial coordinates from initial_coords_dict
            coords = initial_coords_dict[filename.split(_)[1]]
            f.writelines(coords)
            f.write('$END')
            f.close()
            continue

        #Get index of 'theory' to replace with proper command
        i               = ctr_f('theory', basic_params)

        #Get proper theory input style from dictionary
        theo            = theory_dict[filename.split(_)[2]]

        #Get list version of tuple basic parameters
        #(its a tuple to protect it from changes)
        params          = list(basic_params)

        #Replace 'theory' with proper input parameter
        params[i]       = basic_params[i].replace('theory', theo)

        #Add numerical gradients in cctyps if not already there
        if 'CCTYP=' in theo:
            if ctr_f(numgrd, params) == -1:
                params[i] += ' NUMGRD=.T.'

        #Add extra input lines needed for SCS-MP2 and CCSD2-T
        if 'CCSD2-T' in filename.split(_)[2]:
            params.insert(ctr_f('$DATA', params)-1,
                          ' $CCINP MAXCC=100 MAXCCL=100 $END\n')
        if 'SCS' in filename.split(_)[2]:
            params.insert(ctr_f('$DATA', params)-1,
                          ' $MP2 SCSPT=SCS $END\n')

        #Fill in basis parameter for GAMESS(us) internal basis sets
        if filename.split(_)[3] in basis_sets:
            i               = ctr_f('=basis', params)
            bset            = filename.split(_)[3]
            if '6-31' in bset:
                pople = (' $BASIS GBASIS=N' + bset.split('-')[1] +
                         ' NGAUSS=6 NDFUNC=' + bset.split('-')[3].strip('d')+
                         ' NPFUNC=' + bset.split('-')[4].strip('p')+
                         ' $END\n')
                if 'pG' in bset:
                    pople = (' $BASIS GBASIS=N' + bset.split('-')[1] +
                             ' NGAUSS=6 NDFUNC=' + bset.split('-')[3].strip('d')+
                             ' NPFUNC=' + bset.split('-')[4].strip('p')+ '\n'+
                             ' DIFFSP=.TRUE. $END\n')
                if 'ppG' in bset:
                    pople = (' $BASIS GBASIS=N' + bset.split('-')[1] +
                             ' NGAUSS=6 NDFUNC=' + bset.split('-')[3].strip('d')+
                             ' NPFUNC=' + bset.split('-')[4].strip('p')+ '\n'+
                             ' DIFFS=.TRUE. DIFFSP=.TRUE. $END\n')
                params[i] = pople
            else:
                params[i]       = params[i].replace('basis', bset)
        #If not internal delete basis line from input file
        else:
            i               = ctr_f('=basis', params)
            del params[i]

        #Write parameters, and project title
        f.writelines(params)
        f.write(proj_title)

        #Get initial coordinates from initial_coords_dict
        coords = initial_coords_dict[filename.split(_)[1]]

        #Using EMSL put in external basis sets
        if filename.split(_)[3] in ebasis_sets:
            basis_name = filename.split(_)[3]
            molecule   = filename.split(_)[1]
            elements   = get_elements(molecule)
            atoms      = [getattr(el,x) for x in elements]
            if basis_name in basis_dict:
                basis_name = basis_dict[basis_name]
            basis = bse.get_basis(basis_name, elements=elements,
                                  fmt='gamess_us', header=False).split('\n')[1:]
            basis[0] = coords[0]

            for atom in atoms:
                name = atom.Name.upper()
                symb = atom.Symbol + str(atom.AtomicNumber)
                i = ctr_f(name, basis) + 1
                x = []
                while (basis[i] != '') and (basis[i] != '$END'):
                    x.append(basis[i]+'\n')
                    i+=1

                tmp = coords.copy()
                j   = 1
                for i in range(len(coords)):
                    if symb == coords[i].split('.')[0].replace(' ',''):
                        tmp[i+j:i+j] = x
                        j+=len(x)
                        tmp[i+j:i+j] = '\n'
                        j+=1
                coords = tmp

        f.writelines(coords)
        f.write('$END')
        f.close()

    return
