"""
This is the autogamess module, a python module designed to automate
optimization, hessian, raman, and VSCF input generation and output
data collection.

Contains the following functions:
                new_project
                opt2hes
                sort_logs
                hes2raman
                get_data
                input_builder


Author: Brian C. Ferrari
"""
    #Configuration (holds Globals)
from .config        import *

    #Functions
from .new_project              import new_project
from .opt2hes                  import opt2hes
from .sort_logs                import sort_logs
from .hes2raman                import hes2raman
from .input_builder            import input_builder
from .fill_spreadsheets        import fill_spreadsheets
from .get_data                 import get_data
from .make_plot                import make_plot
from .generate_scaling_factors import generate_scaling_factors

    #Multi-function Modules
from .data_finder       import *
