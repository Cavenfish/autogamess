from .config import *
from .data_finder import *

class DATA:
    def __init__(self):
        return

def get_data(filename):
    data    = DATA()

    if '_opt' in filename:
        setattr(data, 'bond_lengths', optimization(filename)[0])
        setattr(data,  'bond_angles', optimization(filename)[1])

    if '_hes' in filename:
        setattr(data, 'vib_freq', hessian(filename)[0])
        setattr(data, 'ir_inten', hessian(filename)[1])

    if '_raman' in filename:
        setattr(data, 'raman', raman(filename))

    if '_vscf' in filename:
        setattr(data, 'vscf_freq', vscf(filename)[0])
        setattr(data,   'vscf_ir', vscf(filename)[1])

    setattr(data,  'cpu', comp(filename)[0])
    setattr(data, 'time', comp(filename)[1])

    return data
