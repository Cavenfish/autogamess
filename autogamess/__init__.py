"""
This is the autogamess module, a python module designed to automate
optimization, hessian, raman, and VSCF input generation and output
data collection.

Contains the following functions:
                new_project
                opt2hes
                sort_logs
                sort_inps
                hes2raman
                input_builder
                fill_spreadsheets
                get_data
                make_plot
                generate_scaling_factors
                convert_ir_units
                make_histogram
                make_scatter


Author: Brian C. Ferrari
"""
    #Configuration (holds Globals)
from .config        import *
from .classes       import *

    #Functions
from .new_project              import new_project
from .opt2hes                  import opt2hes
from .sort_logs                import sort_logs
from .sort_inps                import sort_inps
from .hes2raman                import hes2raman
from .input_builder            import input_builder
from .fill_spreadsheets        import fill_spreadsheets
from .get_data                 import get_data
from .make_plot                import make_plot
from .generate_scaling_factors import generate_scaling_factors
from .convert_ir_units         import convert_ir_units

    #Multi-function Modules
from .data_finder       import *
from .plots             import *
