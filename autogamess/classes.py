from .dictionaries import templates
from .config       import version, read_file

#Class for input parameters
class INPUT:
    'GAMESS(US) input parameters'

    #--------------------------CONTROL--------------------------------
    class Control:
        'Control class of GAMESS(US) input'

        def __init__(self):
            pass

        def make_string(self):
            s = ' $CONTROL '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                add_this = i.upper() + '=' + self.__dict__[i] + ' '
                if n + len(add_this) > 50:
                    s += '\n '
                    n  = 0
                s += add_this
                n += len(add_this)

            s += e
            return s

    #--------------------------SYSTEM--------------------------------
    class System:
        'System class of GAMESS(US) input'

        def __init__(self):
            pass

        def make_string(self):
            s = ' $SYSTEM '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                add_this = i.upper() + '=' + self.__dict__[i] + ' '
                if n + len(add_this) > 50:
                    s += '\n '
                    n  = 0
                s += add_this
                n += len(add_this)

            s += e
            return s

    #--------------------------STATPT--------------------------------
    class Statpt:
        'Statpt class of GAMESS(US) input'

        def __init__(self):
            pass

        def make_string(self):
            s = ' $STATPT '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                add_this = i.upper() + '=' + self.__dict__[i] + ' '
                if n + len(add_this) > 50:
                    s += '\n '
                    n  = 0
                s += add_this
                n += len(add_this)

            s += e
            return s

    #--------------------------SCF--------------------------------
    class Scf:
        'SCF class of GAMESS(US) input'

        def __init__(self):
            pass

        def make_string(self):
            s = ' $SCF '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                add_this = i.upper() + '=' + self.__dict__[i] + ' '
                if n + len(add_this) > 50:
                    s += '\n '
                    n  = 0
                s += add_this
                n += len(add_this)

            s += e
            return s

    #--------------------------DFT--------------------------------
    class Dft:
        'DFT class of GAMESS(US) input'

        def __init__(self):
            pass

        def make_string(self):
            s = ' $DFT '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                add_this = i.upper() + '=' + self.__dict__[i] + ' '
                if n + len(add_this) > 50:
                    s += '\n '
                    n  = 0
                s += add_this
                n += len(add_this)

            s += e
            return s

    #--------------------------BASIS--------------------------------
    class Basis:
        'Basis class of GAMESS(US) input'

        def __init__(self):
            pass

        def make_string(self):
            s = ' $BASIS '
            e = '$END\n'
            n = len(s)
            for i in self.__dict__:
                add_this = i.upper() + '=' + self.__dict__[i] + ' '
                if n + len(add_this) > 50:
                    s += '\n '
                    n  = 0
                s += add_this
                n += len(add_this)

            s += e
            return s


    #--------------------------INPUT funtions--------------------------------
    def __init__(self, template):

        if ('.txt' in template) or ('.inp' in template):
            self.read_txt(template)
        else:
            self.defaults(template)

    def read_txt(self, txtfile):

        inp = read_file(txtfile)

        inp = ''.join(inp)

        inp = inp.replace('\n', '')

        inp = inp.split('$END')

        for i in inp:
            if '$' not in i:
                continue
            i = i.split('$')[1].split()
            group_name = i[0].capitalize()
            params     = i[1:]
            obj        = getattr(self, group_name)
            for j in params:
                j   = j.split('=')
                key = j[0].lower()
                val = j[1]
                setattr(obj, key, val)

    def defaults(self, template):
        params       = templates[template]
        self.Control = self.Control(params['Control'])
        self.System  = self.System( params['System'] )
        self.Statpt  = self.Statpt( params['Statpt'] )
        self.SCF     = self.SCF(    params['SCF']    )
        self.DFT     = self.DFT()
        self.Basis   = self.Basis()

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
