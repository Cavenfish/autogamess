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
    numgrd  = 'NUMGRD=.T.'

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
            atoms      = [getattr(el,x) for x in molecule if x.isupper() and x.isalpha()]
            elements   = [x for x in molecule if x.isupper() and x.isalpha()]
            if basis_name in basis_dict:
                basis_name = basis_dict[basis_name]
            basis = bse.get_basis(basis_name, elements=elements,
                                  fmt='gamess_us', header=False).split('\n')[1:]
            basis[0] = coords[0]

            for atom in atoms:
                name = atom.Name.upper()
                symb = atom.Symbol
                i = ctr_f(name, basis)
                j = ctr_f(symb, coords[a:]) + a
                basis[i] = coords[j].strip('\n')
                a=j

            basis[-1] = '\n' + basis[-1]
            f.write('\n'.join(basis))
            f.close()
        else:
            f.writelines(coords)
            f.write('$END')
            f.close()

    return
