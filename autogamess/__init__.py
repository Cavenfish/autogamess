"""
This is the autogamess module, a python module designed to automate
optimization, hessian, raman, and VSCF input generation and output
data collection.

Contains the following functions:
                bat_maker
                new_project
                opt2hes
                sort_logs
                hes2raman
                get_data


Author: Brian C. Ferrari
"""
from .config        import *              #Configuration (holds Globals)

from .bat_maker     import bat_maker      #Functions
from .new_project   import new_project
from .opt2hes       import opt2hes
from .sort_logs     import sort_logs
from .hes2raman     import hes2raman
from .input_builder import input_builder

from .get_data      import *              #Multi-function Modules
