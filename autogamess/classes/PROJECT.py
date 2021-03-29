from ..config       import *
from ..dictionaries import *
import elements.elements as el
import basis_set_exchange as bse
from copy import deepcopy

#----------------------PROJECT CLASS--------------------------------------
class PROJECT:
    'AutoGAMESS Project Class'

    def __init__(self):
        self.title      = ''
        self.species    = []
        self.theories   = []
        self.comp_meths = []
        self.basis_sets = []
        self.ext_basis  = []
        self.run_types  = []
        self.map        = {}

    def make_project(self, maindir, safety_check=False):
        """
        This function creates a new directory tree for a GAMESS project, also makes
        a couple of text files for use with other functions.

        Parameters
        ----------
        maindir: string
            A directory string (including the final `/`) that points to the
            directory that the project tree will be spawned in.
        safety_check: boolean True/False [Optional]
            if True then input files will be internal reviewed by AutoGAMESS.

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
        """
        self.make_dir_tree(maindir)
        projdir = maindir + self.title + '/'
        self.build_inps(projdir, safety_check=safety_check)

    def make_dir_tree(self, maindir):
        #Defining directory names
        unsolved = maindir + self.title + '/Logs/Fail/Unsolved/'
        solved   = maindir + self.title + '/Logs/Fail/Solved/'
        xldir    = maindir + self.title + '/Spreadsheets/'
        inputs   = maindir + self.title + '/Inps/'
        goodlogs = maindir + self.title + '/Logs/Pass/'
        sorrted  = maindir + self.title + '/Logs/Sorted/'

        #Define random commands
        fin      = '\nBREAK\n'
        engine   = 'xlsxwriter'
        xlsx     = '.xlsx'

        #Make directories
        try:
            os.makedirs(unsolved)
            os.makedirs(solved)
            os.makedirs(xldir)

            #Make Block directory trees
            for runtyp in self.run_types:
                runtyp += '/'
                for specie in self.species:
                    specie += '/'
                    os.makedirs(inputs+runtyp+specie)
                    os.makedirs(goodlogs+runtyp+specie)
        except:
            print(error_head)
            print("One or more directories in Project tree already exist")
            print(error_tail)

        #Make data for Spreadsheets
        theo = []
        for theory in self.theories:
            temp    = [theory]*len(self.basis_sets + self.ext_basis)
            theo   += temp + ['\n', '\n','\n']

        bs = (self.basis_sets + self.ext_basis
              + ['\n', '\n','\n']) *len(self.theories)

        #Make dataframe with theory and basis sets names only
        data = {   'Theory': theo,
                'Basis Set': bs}
        df2  = pd.DataFrame(data=data)

        #Make data for Composite method Sheets
        data = {'Method': self.comp_meths}
        df3  = pd.DataFrame(data=data)

        #More directory making and Excell workbook and sheet making
        for specie in self.species:
            specie += '/'
            os.makedirs(sorrted+specie)

            #Define header for Spreadsheets
            header = [version, author, '',
                      'Project Name : ' +  self.title,
                      'Molecule Name: ' + specie.replace('/', '')]

            #Define Excell filename
            xlfilename = xldir + specie.replace('/', xlsx)

            #Initialize writer
            writer = pd.ExcelWriter(xlfilename, engine=engine)

            #Make Sheets and put headers on them all
            for runtyp in self.run_types:
                runtyp += '/'

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
                bl = 'Bond Length (Å)'
                ba = 'Bond Angle (degrees)'
                vf = 'Vibrational Frequency (cm⁻¹)'
                ii = 'Infrared Intensity (km mol⁻¹)'
                ra = 'Raman Activity (angstrom⁴ amu⁻¹)'
                fv = 'VSCF Frequency (cm⁻¹)'
                iv = 'VSCF IR (km mol⁻¹)'
                hf = 'Heat of Formation (kcal mol⁻¹)'
                sb = '          '
                if runtyp == 'Optimization/':
                    worksheet.write(2, 0, u + sb + bl + sb + ba)
                if runtyp == 'Hessian/':
                    worksheet.write(2, 0, u + sb + vf + sb + ii)
                if runtyp == 'Raman/':
                    worksheet.write(2, 0, u + sb + ra)
                if runtyp == 'VSCF/':
                    worksheet.write(2, 0, u + sb + fv + sb + iv)
                if runtyp == 'Composite/':
                    worksheet.write(2, 0, u + sb + hf)

            #Save Excell file
            writer.save()

    def make_file_name(self, specie, inp):
        theory = inp.theory
        basis  = inp.basis_set

        if len(inp.Contrl.runtyp) > 5:
            if inp.Contrl.runtyp == 'COMPOSITE':
                run_name = 'comp'
            run_name  = inp.Contrl.runtyp[0:3].lower()
        else:
            run_name  = inp.Contrl.runtyp.lower()

        file_name = agv + '_' + specie + '_' + theory + '_'  + \
                    basis + '_' + run_name + '.inp'

        return file_name

    def build_inps(self, savedir, safety_check=False):

        #Molecule Iterator
        for specie in self.species:

            #Theory Level Iterator
            for theory in self.theories:

                #Internal Basis Set Iterator
                for basis in self.basis_sets:
                    inp            = deepcopy(self.map[specie])   #Get Template
                    inp.Data.title = self.title                   #Add Title
                    inp.prep_template()                           #Prep Template
                    inp.theory = theory                           #Def Theory Global
                    theo = theory_dict[theory].split('=')         #Prep it
                    setattr(inp.Contrl, theo[0].lower(), theo[1]) #Add it

                    inp.basis_set    = basis #Define Basis Set Global
                    inp.Basis.gbasis = basis #Add Basis Set to Inp

                    #Delete external basis set
                    if inp.basis_set:
                        inp.basis_set = {}

                    #Run type and file naming
                    inp.run_type = inp.Contrl.runtyp.lower()
                    file_name    = self.make_file_name(specie, inp)

                    if safety_check:
                        inp.check()
                    inp.write_inp(savedir + file_name)


                #External Basis Set Iterator
                for basis in self.ext_basis:
                    inp            = deepcopy(self.map[specie])   #Get Template
                    inp.Data.title = self.title                   #Add Title
                    inp.prep_template()                           #Prep Template
                    inp.theory = theory                           #Def Theory Global
                    theo = theory_dict[theory].split('=')         #Prep it
                    setattr(inp.Contrl, theo[0].lower(), theo[1]) #Add it

                    #Delete GAMESS(US) internal Basis Set group
                    if hasattr(inp, 'Basis'):
                        delattr(inp, 'Basis')

                    inp.basis_set = basis
                    file_name     = self.make_file_name(specie, inp)
                    inp.Data.add_basis(basis)

                    if safety_check:
                        inp.check()
                    inp.write_inp(savedir + file_name)

                #Remove External Basis set from inp
                inp.Data.basis = {}
