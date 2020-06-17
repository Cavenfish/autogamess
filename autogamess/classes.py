from .dictionaries import *
import elements.elements as el
import basis_set_exchange as bse
from .config       import version, read_file

#Class for input parameters
class INPUT:
    'GAMESS(US) input parameters'

    class Param_Group:
        'Subclass for GAMESS(US) input parameter groups'

        def __init__(self, name):
            self.name = name

        def make_string(self):
            s = ' $' + self.name.upper() + ' '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                if i is 'name':
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
            self.name   = None
            self.sym    = None
            self.coords = []
            self.basis  = {}

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
                    s   += line + self.basis[atom] + '\n\n'
                s += e
                return s

            s += ''.join(self.coords) + e
            s += e
            return s


    #--------------------------INPUT funtions--------------------------------
    def __init__(self, template):

        if template in templates:
            inp = templates[template]
        else:
            inp = read_file(template)
            inp = ''.join(inp)
            inp = inp.replace('\n', '')

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

    def write_inp(self, file_name):
        f = open(file_name, 'w')
        f.write('!'+ version +'\n')
        f.write('!  by Brian C. Ferrari \n')
        f.write('!\n')

        for i in self.__dict__:
            try:
                f.write(getattr(self, i).make_string())
            except:
                continue

        f.close()
