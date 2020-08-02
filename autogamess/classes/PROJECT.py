from ..config       import *
from ..dictionaries import *
import elements.elements as el
import basis_set_exchange as bse

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
        self.templates  = {}

    def make_project(self):
        self.make_dir_tree()
        self.make_inps()

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

    def build_inps(self, savedir, safety_check=False):

        for specie in self.species:
            inp            = self.map[specie]
            inp.Data.title = self.title

            for theory in self.theories:
                theo = theory_dict[theory].split('=')

                try:
                    delattr(inp.Contrl, 'dfttyp')
                except:
                    pass
                try:
                    delattr(inp.Contrl, 'cctyp')
                except:
                    pass
                try:
                    delattr(inp.Contrl, 'mplevl')
                except:
                    pass

                setattr(inp.Contrl, theo[0].lower(), theo[1])

                if int(inp.Contrl.mult) > 1:
                    if 'CCSD2-T' in theory:
                        inp.Contrl.scftyp = 'ROHF'
                    if 'CCSD-T' in theory:
                        inp.Contrl.scftyp = 'UHF'

                if ('B3LYP' in theory) and (~hasattr(inp, 'Dft')):
                    inp.Dft      = inp.Param_Group('Dft')
                    inp.Dft.jans = '2'

                if ('SCS-MP2' in theory) and (~hasattr(inp, 'Mp2')):
                    inp.Mp2       = inp.Param_Group('Mp2')
                    inp.Mp2.scspt = 'SCS'
                    inp.Mp2.code  = 'IMS'

                if ('CCSD2-T' in theory) and (~hasattr(inp, 'Ccinp')):
                    inp.Ccinp        = inp.Param_Group('Ccinp')
                    inp.Ccinp.maxcc  = '100'
                    inp.Ccinp.maxccl = '100'

                if ('B3LYP' not in theory) and (hasattr(inp, 'Dft')):
                    delattr(inp, 'Dft')

                if ('SCS-MP2' not in theory) and (hasattr(inp, 'Mp2')):
                    delattr(inp, 'Mp2')

                if ('CCSD2-T' not in theory) and (hasattr(inp, 'Ccinp')):
                    delattr(inp, 'Ccinp')

                for basis in self.basis_sets:
                    try:
                        delattr(inp, 'Basis')
                        inp.Basis = inp.Param_Group('Basis')
                    except:
                        inp.Basis = inp.Param_Group('Basis')

                    inp.Basis.gbasis = basis
                    run_name  = inp.Contrl.runtyp[0:3].lower()
                    file_name = agv + '_' + specie + '_' + theory + '_'  + \
                                basis + '_' + run_name + '.inp'

                    if safety_check:
                        self.check(inp)
                    inp.write_inp(savedir + file_name)

                for basis in self.ext_basis:
                    try:
                        delattr(inp, 'Basis')
                    except:
                        pass

                    inp.Data.add_basis(basis)
                    run_name  = inp.Contrl.runtyp[0:3].lower()
                    file_name = agv + '_' + specie + '_' + theory + '_'  + \
                                basis + '_' + run_name + '.inp'

                    if safety_check:
                        self.check(inp)
                    inp.write_inp(savedir + file_name)

                try:
                    inp.Data.basis = {}
                except:
                    pass
