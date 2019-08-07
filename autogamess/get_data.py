from .config import *
from .data_finder import *

class DATA:
    def __init__(self):
        return

def get_data(filename):
    """
    This function collects data from GAMESS(us) log files.

    Parameters
    ----------
    filename: string
        This should be a string that points to the log file of any
        GAMESS(us) calculation. (FULL DIRECTORY STRING REQUIRED)

    Returns
    -------
    data: object
        This is an object with all the data collected from the log file.
        Below is a list of the attributes associated with `data` based on
        each log file type. 

        all   files: `cpu`, `time`
        opt   files: `bond_lengths`, `bond_angles`
        hes   files: `vib_freq`, `ir_inten`
        raman files: `raman`
        vscf  files: `vscf_freq`, vscf_ir

    Notes
    -------
    This function is primarily intended for interal use by AutoGAMESS.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> filename = './AGv0-0-6_NH3_CCSD-T_CC6_opt.log'
    >>>
    >>> ag.get_data(filename)
    >>>
    """
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
