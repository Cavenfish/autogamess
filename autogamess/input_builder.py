from .config import *
import pkg_resources
from .molecule_dictionary import molecule_dictionary

def input_builder(inputfile, initial_coords_dict=molecule_dictionary,
                  ebasis_dir, save_dir, proj_title=' Your Title Goes Here\n'):
    '''
    This function build optimization input files.
    '''
    _       = '_'
    version = (' AutoGAMESS Version ' +
                str(pkg_resources.require("autogamess")[0].version) )
    ibv     = 'AGv' + version.split(' ')[-1].replace('.', '-')
    opt     = '_opt.inp'

    df = pd.read_csv(inputfile)

    species     = list(df['Species'].dropna())
    theories    = list(df['Theory'].dropna())
    basis_sets  = list(df['Basis Sets'].dropna())
    ebasis_sets = list(df['External Basis Sets'].dropna())

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





    for filename in files:
        f = open(save_dir + filename, 'w')
        f.write('!'+ version +'\n')
        f.write('!  by Brian C. Ferrari \n')
        f.write('!\n')

        i               = ctr_f('theory', basic_params)
        theo            = theory_dict[filename.split(_)[2]]
        params          = list(basic_params)
        params[i]       = basic_params[i].replace('theory', theo)

        if filename.split(_)[3] in basis_sets:
            i               = ctr_f('=basis', basic_params)
            bset            = filename.split(_)[3]
            params[i]       = basic_params[i].replace('basis', bset)
        else:
            i               = ctr_f('=basis', basic_params)
            del params[i]


        f.writelines(params)
        f.write(proj_title)

        coords = initial_coords_dict[filename.split(_)[1]]

        if filename.split(_)[3] in ebasis_sets:
            f2   = open(ebasis_dir + filename.split(_)[3] + '.txt', 'r')
            temp = f2.readlines()
            f2.close()

            for coord in coords:
                find    = coord.split('  ')[0]
                i       = ctr_f(find, temp)
                if i is -1:
                    continue
                temp[i] = coord

            f.writelines(coords[0:2])
            f.writelines(temp)

        else:
            f.writelines(coords)

        f.write(' $END')
        f.close()
