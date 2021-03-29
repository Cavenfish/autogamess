from ..config      import *
from ..dictionaries import *
import elements.elements as el
import basis_set_exchange as bse

#Class for input parameters
class INPUT:
    'GAMESS(US) input parameters'

    theory    = ''
    basis_set = ''
    run_type  = ''

    class Param_Group:
        'Subclass for GAMESS(US) input parameter groups'

        def __init__(self, name):
            self.name = name

        def make_string(self):
            s = ' $' + self.name.upper() + ' '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                if i == 'name':
                    continue
                add_this = i.upper() + '=' + self.__dict__[i] + ' '
                if n + len(add_this) > 50:
                    s += '\n '
                    n  = 0
                s += add_this
                n += len(add_this)

            s += e
            return s

    class Data_Group:
        'Subclass for GAMESS(US) Data Input group'

        def __init__(self):
            self.title  = ''
            self.sym    = None
            self.coords = []
            self.basis  = {}

        def read_inp(self, inp):
            i = inp.split('$DATA')[1].split('\n')
            s = ctr_f(  '.0', i)
            e = ctr_f('$END', i)
            self.sym    = i[2]
            self.title  = i[1]

            n = False
            for line in i[3:]:
                j = len(line.split())
                if ((j == 5) and n) or (('$END' in line) and n):
                    m    = i.index(line) - 1
                    if m == n:
                        continue
                    self.basis[atom] = '\n'.join(i[n:m])
                    n    = False
                if j == 5:
                    self.coords.append(line)
                    atom = line.split()[0]
                    n    = i.index(line) + 1


        def get_elements(self):
            elements = []
            for line in self.coords:
                x = line.split()[0]
                if x not in elements:
                    elements.append(x)

            return elements

        def add_basis(self, basis_name):
            if basis_name in basis_dict:
                basis_name = basis_dict[basis_name]

            elements  = self.get_elements()
            atoms     = [getattr(el,x) for x in elements]
            basis_set = bse.get_basis(basis_name, elements=elements,
                                      fmt='gamess_us', header=False)

            atoms.sort(key=lambda x: x.AtomicNumber)
            for i in range(len(atoms)):
                name1 = atoms[i].Name.upper()

                try:
                    name2 = atoms[i+1].Name.upper()
                except:
                    name2 = '$END'

                a                           = basis_set.find(name1) + len(name1)
                b                           = basis_set.find(name2)
                atom_basis                  = basis_set[a:b]
                self.basis[atoms[i].Symbol] = atom_basis[1:].strip('\n')

            return

        def make_string(self):
            s = ' $DATA\n'

            if self.title:
                if self.title[0] != ' ':
                    s += ' ' + self.title + '\n'
                s += self.title + '\n'

            e = '$END'

            if '\n' in self.sym:
                s += self.sym
            else:
                if 'C1' in self.sym:
                    s += self.sym + '\n'
                else:
                    s += self.sym + '\n\n'


            if self.basis:
                for line in self.coords:
                    atom = line.split()[0]
                    if '\n' not in line:
                        line += '\n'
                    s   += line + self.basis[atom] + '\n\n'
                s += e
                return s

            if '\n'not in self.coords:
                s += '\n'.join(self.coords)
                s += '\n'
            else:
                s += ''.join(self.coords)
            s += e
            return s


    #--------------------------INPUT funtions--------------------------------
    def __init__(self, template):

        if template in templates:
            inp = templates[template]
        else:
            inp  = read_file(template)
            inp  = ''.join(inp)
            data = inp
            inp  = inp.replace('\n', '')

        inp = inp.split('$END')
        for i in inp:
            if '$' not in i:
                continue

            if '$DATA' in i:
                continue

            i                             = i.split('$')[1].split()
            group_name                    = i[0].capitalize()
            params                        = i[1:]
            exec('self.' + group_name + ' = self.Param_Group(group_name)')
            for j in params:
                j   = j.split('=')
                key = j[0].lower()
                val = j[1]
                exec('setattr(self.' + group_name + ', key, val)')

        self.Data = self.Data_Group()
        self.Data.read_inp(data)

    def write_inp(self, file_name):
        f = open(file_name, 'w')
        f.write('!'+ version +'\n')
        f.write('!  by Brian C. Ferrari \n')
        f.write('!\n')

        for i in self.__dict__:
            if 'Data' in i:
                continue

            try:
                f.write(getattr(self, i).make_string())
            except:
                continue

        try:
            f.write(getattr(self, 'Data').make_string())
        except:
            pass

        f.close()

    def prep_template(self):
        #Remove Theory Level command form input template
        stuff2delete = ['dfttyp', 'cctyp', 'mplevl']
        for i in stuff2delete:
            try:
                delattr(self.Contrl, i)
            except:
                pass

        #Remove Basis Set group from input template & generate blank one
        try:
            delattr(self, 'Basis')
            self.Basis = self.Param_Group('Basis')
        except:
            self.Basis = self.Param_Group('Basis')

    def check(self):
        #Remove spherical coordinates if Pople basis set in use
        if '6-31' in self.basis_set:
            try:
                delattr(self.Contrl, 'ispher')
            except:
                pass

        #Ensure CC types have FULLNUM and numgrd
        if hasattr(self.Contrl, 'cctyp'):
            self.Contrl.numgrd = '.T.'
            if not hasattr(self, 'Force'):
                self.Force = self.Param_Group('Force')
            self.Force.method = 'FULLNUM'
            self.Force.nvib   = '2'
            self.Force.projct = '.T.'

        #Add force card for hessians
        if self.Contrl.runtyp == 'HESSIAN':
            if not hasattr(self, 'Force'):
                self.Force = self.Param_Group('Force')
            self.Force.method = 'SEMINUM'
            self.Force.nvib   = '2'
            self.Force.projct = '.T.'

            if hasattr(self.Contrl, 'numgrd'):
                delattr(self.Contrl, 'numgrd')

            if hasattr(self.Contrl, 'cctyp'):
                self.Force.method = 'FULLNUM'

        #Inlcude Jans=2 grid for all DFT functionals
        if hasattr(self.Contrl, 'dfttyp'):
            if  not hasattr(self, 'Dft'):
                self.Dft      = self.Param_Group('Dft')
                self.Dft.jans = '2'
            else:
                self.Dft.jans = '2'

        #Ensure that SCS and IMS commands are included for SCS-MP2
        if 'SCS-MP2' in self.theory:
            if not hasattr(self, 'Mp2'):
                self.Mp2       = self.Param_Group('Mp2')
                self.Mp2.scspt = 'SCS'
                self.Mp2.code  = 'IMS'
            else:
                self.Mp2.scspt = 'SCS'
                self.Mp2.code  = 'IMS'

        #Raise max iteration of CCSD and left eigenstate for CCSD(2)T
        if 'CCSD2-T' in self.theory:
            if not hasattr(self, 'Ccinp'):
                self.Ccinp        = self.Param_Group('Ccinp')
                self.Ccinp.maxcc  = '100'
                self.Ccinp.maxccl = '100'
            else:
                self.Ccinp.maxcc  = '100'
                self.Ccinp.maxccl = '100'

        #Remove DFT group from non-DFT calculations
        if (not hasattr(self.Contrl, 'dfttyp')) and (hasattr(self, 'Dft')):
            delattr(self, 'Dft')

        #Remove MP2 group from non-MP calculations
        if (not hasattr(self.Contrl, 'mplevl')) and (hasattr(self, 'Mp2')):
            delattr(self, 'Mp2')

        #Remove CCinp group from non-CC calculations
        if (not hasattr(self.Contrl, 'cctyp')) and (hasattr(self, 'Ccinp')):
            delattr(self, 'Ccinp')
