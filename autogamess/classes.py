from .dictionaries import templates
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

    #--------------------------INPUT funtions--------------------------------
    def __init__(self, template):

        if template in templates:
            inp = templates[template]
        else:
            inp = read_file(txtfile)
            inp = ''.join(inp)
            inp = inp.replace('\n', '')

        inp = inp.split('$END')
        for i in inp:
            if '$' not in i:
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
