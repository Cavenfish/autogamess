import pytest

def test_numpy_import():
    import numpy

    return


def test_scipy_import():
    import scipy

    return


def test_pandas_import():
    import pandas

    return

def test_basis_set_exchange_import():
    import basis_set_exchange

    return


def test_elements_import():
    import elements.elements

    return


def test_openpyxl_import():
    import openpyxl

    return


def test_autogamess_module():
    import autogamess
    from autogamess import new_project
    from autogamess import opt2hes
    from autogamess import sort_logs
    from autogamess import hes2raman
    from autogamess import input_builder
    from autogamess import fill_spreadsheets
    from autogamess import get_data


if __name__ == "__main__":
    test_numpy_import()
    test_scipy_import()
    test_pandas_import()
    test_elements_import()
    test_openpyxl_import()
    test_basis_set_exchange_import()
    test_pycurious_modules()
