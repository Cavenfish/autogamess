# AutoGAMESS

This is a python module for automating Raman calculations using the [GAMESS(us)](https://www.msg.chem.iastate.edu/gamess/) Quantum Chemistry software.

# Installing AutoGAMESS

AutoGAMESS can be installed using

`python -m pip install autogamess --user`

AutoGAMESS requires all the following Python packages:

* Python3.x
* NumPy
* SciPy
* Pandas
* basis_set_exchange
* PeriodicElements
* openpyxl

# Tests

AutoGAMESS uses pytest for testing, from within the tests directory execute the following to run tests.

`python -m pytest`

# Function Documentations

### new_project
**`new_project(maindir,csvfile,initial_coords_dict=None,title='Project_Name/', make_inputs=False)`**

```
This function creates a new directory tree for a GAMESS project, also makes
  a couple of text files for use with other functions.

  Parameters
  ----------
  maindir: string
      A directory string (including the final `/`) that points to the
      directory that the project tree will be spawned in.
  csvfile: string
      A directory string (including the final `.csv`) that points to the
      text file containing project information. Read module documentation
      for csv file format.
  initial_coords_dict: dictionary [Optional]
      This should be a dictionary with the key being the specie and the
      value being a list that of its initial coordinates.
  title: string [Optional]
      A directory string (including the final `/`) that will be used as
      the head of project directory tree.
  make_inputs: boolean True/False [Optional]
      if True then new_project will call input_builder at the end.

  Notes 1
  ----------
  If the molecules you wish to build are not already defined in the
  general autogamess coordinate dictionary, then initial_coords_dict
  must be passed.

  To see the autogamess coordinate dictionary simply print out
  >>> ag.dictionaries.molecule_dictionary

  Returns
  ----------
  This function returns nothing

  Notes 2
  ----------
  The format of the spawned directory tree is as follows:

                                  maindir
                                     |
                                   title
                      -------------------------------------
                      |        |        |        |        |
                    Codes    Inps     Logs  Batch_Files  Spreadsheets
                      |        |        |                     |
                ---------    Block    -----------      1 file per specie
                |       |             |    |    |
          Text_Files  Scripts      Fail   Pass  Sorted
                                    |      |        |
                                 -------  Block   1 directory per specie
                                 |     |
                           Unsolved   Solved


  Sections in directory tree labeled 'Block' are directory trees with the
  following format:
                    1 directory per run type
                                |
                    1 directory per specie

  Examples
  ----------
  >>> import autogamess as ag
  >>>
  >>> csvfile = './input.csv'
  >>> maindir = './'
  >>> title   = 'Project Title/'
  >>>
  >>> ag.new_project(maindir, csvfile, title=title)
  >>>
```

### input_builder

**`input_builder(inputfile, save_dir, initial_coords_dict=None,proj_title=' Your Title Goes Here\n')`**

```
This function builds optimization input files.

Parameters
----------
inputfile: string
    This should be a full directory string that points to the input
    csv file.
save_dir: string
    this should be a full directory string that points to the directory
    you wish to save the inputs in.
initial_coords_dict: dictionary [Optional]
    This should be a dictionary with the key being the specie and the
    value being a list that of its initial coordinates.
proj_title: string [Optional]
    This should be a string ending with `\n`

Notes 1
----------
If the molecules you wish to build are not already defined in the
general autogamess coordinate dictionary, then initial_coords_dict
must be passed.

To see the autogamess coordinate dictionary simply print out
>>> ag.dictionaries.molecule_dictionary

Returns
----------
This function returns nothing

Notes 2
----------
This function uses the EMSL Basis Set Exchange module to import
external basis sets[1]. This function also uses the Periodic_Elements
package by VaasuDevanS [2].

[1] https://github.com/MolSSI-BSE/basis_set_exchange
[2] https://github.com/VaasuDevanS/Periodic_Elements


Examples
----------
>>> import autogamess as ag
>>>
>>> csvfile = './input.csv'
>>> savedir = './'
>>> title   = 'Project\n'
>>>
>>> ag.input_builder(csvfile, savedir, proj_title=title)
>>>
```

### opt2hes

**`opt2hes(optfile, logfile)`**

```
This function writes a hessian calculation input file using a previously
run optimization input file and the log file generated by the calculation.

Parameters
----------
optfile: string
    This should be a string that points to the input file of an
    already run optimization file. (FULL DIRECTORY STRING REQUIRED)
logfile: string
    This should be a string that points to the log file of an
    already run optimization file. (FULL DIRECTORY STRING REQUIRED)

Returns
-------
This function returns nothing if it terminates successfully, otherwise
it returns ValueError.

Example
-------
>>> import autogamess as ag
>>>
>>> logfile = './Optimization_Log_Folder/IBv6_NH3_CCSD-T_CC6_opt.log'
>>> optfile = './IBv6_NH3_CCSD-T_CC6_opt.inp'
>>>
>>> ag.opt2hes(optfile, logfile)
>>>
```

### hes2raman

**`hes2raman(hesfile, datfile)`**

```
This function writes a raman calculation input file using a previously
run hessian input file and the dat file generated by the calculation.

Parameters
----------
hesfile: string
    This should be a string that points to the input file of an
    already run hessian file. (FULL DIRECTORY STRING REQUIRED)
datfile: string
    This should be a string that points to the DAT file of an
    already run hessian file. (FULL DIRECTORY STRING REQUIRED)

Returns
-------
This function returns nothing if it terminates successfully, otherwise
it returns ValueError.

Example
-------
>>> import autogamess as ag
>>>
>>> datfile = '../restart/IBv6_NH3_CCSD-T_CC6_hes.dat'
>>> hesfile = './IBv6_NH3_CCSD-T_CC6_hes.inp'
>>>
>>> ag.hes2raman(hesfile, datfile)
>>>
```

### sort_logs

**`sort_logs(projdir, logsdir)`**

```
This function sorts all the loose log files in the 'Logs' directory.

Parameters
----------
projdir: string
    A directory string (including the final `/`) that points to the
    project head directory.
logsdir: string
    A directory string (including the final `/`) that points to the
    directory containing the log files.

Returns
----------
This function returns nothing

Notes
----------
For this function to work properly the project directory tree must be
in the exact format that the 'new_project' function spawned it in.

Examples
----------
>>>import sort_logs
>>>projdir = './Example/'
>>>sort_logs(projdir)
>>>
```

### fill_spreadsheets

**`fill_spreadsheets(projdir=False, sorteddir=False, sheetsdir=False)`**

```
This function fills in the spreadsheets initially generated by new_project
with data collected from the outfiles of calculations.

Parameters
----------
projdir: string [Optional]
    This should be a full directory string pointing to the project
    directory initially created by new_project.
sorteddir: string [Optional]
    This should be a full directory string pointing to the sorted log
    files directory.
sheetsdir: string [Optional]
    This should be a full directory string pointing to the spreadsheets
    directory.

Notes
----------
If projdir is not passed to fill_spreadsheets function then both other
parameters MUST be passed to it. Similarly if projdir is passed the
other two parameters MUST be left blank.

Returns
-------
This function returns nothing.

Example
-------
>>> import autogamess as ag
>>>
>>> projdir = './Your Project Title/'
>>>
>>> ag.fill_spreadsheets(projdir)
>>>

>>> import autogamess as ag
>>>
>>> sorteddir = './project/Logs/Sorted/'
>>> sheetsdir = './project/Spreadsheets/'
>>>
>>> ag.fill_spreadsheets(sorteddir=sorteddir, sheetsdir=sheetsdir)
>>>
```

# Input Descriptions
All user functions contain doc strings with examples and explanations of parameters and returns. However, a few functions require specific inputs not fully explained in the doc strings. Such as the functions:
* new_project
* input_builder

The CSV file required by both functions must have the following format. The first line must be the header, written exactly as follows.

| Species | Theory | Basis Sets | External Basis Sets | Run Types |
| ------- | ------ | ---------- | ------------------- | --------- |

All lines after the header should give input as 1 item per column per line. As shown in the example bellow.

| Species | Theory  | Basis Sets | External Basis Sets | Run Types    |
| ------- | ------  | ---------- | ------------------- | ---------    |
| H2O     | B3LYP   | CCD        | may-cc-pVDZ         | Optimization |
| NH3     | MP2     | CCT        | aug-cc-pV7Z         | Hessian      |
| HCN     | CCSD-T  | CCQ        | may-cc-pVTZ         | Raman        |
| H2CO    | PBE     | CC5        | Sadlej-pVTZ         | VSCF         |
| CH4     | wB97X-D | CC6        | jun-cc-pVQZ         |              |
| C2H6    | SCS-MP2 | ACCD       | jul-cc-pVTZ         |              |
| C2H4    | CCSD2-T | ACCT       |                     |              |
| C2H2    |         | ACCQ       |                     |              |


Internal basis sets should be written in the same format as they are required by GAMESS(us) inputs.

External basis sets should be written in the same format as they as required by ESML [basis_set_exchange](https://github.com/MolSSI-BSE/basis_set_exchange). Some external basis sets have shorthand names built into AutoGAMESS to prevent special characters such as `(, ), +, etc.` from being put into file names. Notice this is applicable to `may-cc-pV(D+d)Z` written simply as `may-cc-pVDZ` similarly for the other calendar basis sets.

initial_coords_dict is another input parameter that requires specific formatting. The dictionary is meant to give the initial guess coordinates for a particular symmetry of a molecule. This should be a python dictionary that has the Species (molecule) name as the key and a list with the following format.

```python
key = 'H2O'

value = ['CnV 2,\n','\n',
         ' O           8.0  -0.0000000000   0.0000000000  -0.0123155409\n',
         ' H           1.0  -0.0000000000  -0.7568005555   0.5926935705\n']

initial_coords_dict = {key : value}
```

Some molecules are already compiled within AutoGAMESS default dictionary however, if one of the molecules in the input CSV file is not within the default dictionary a complete dictionary with all molecules within the CSV file is required by AutoGAMESS.

# Examples of Common AutoGAMESS Utilization Methods

A basic script for generating a new project directory, sorting already existing logs into it, then filling the spreadsheets with the data in the existing output files. For this script to work properly, file names must adhere to the AutoGAMESS file naming convention

`[arbitrary thing]_[Specie]_[Theory Level]_[Basis Set]_[Abbreviated Run Type].[inp/log/dat]`

The 'arbitrary thing' section can be anything, since this is typically where AutoGAMESS will write the version number. Since AutoGAMESS reads information from file names and requires the underscore separates the information something must be present there to prevent confusion. The Abbreviated Run Types are,

`Optimization = opt`

`Hessian = hes`

`Raman = raman`

`VSCF =  vscf`

```python
import autogamess as ag

maindir = './'
csvfile = './input.csv'
title   = 'Project Title/'

ag.new_project(maindir, csvfile, title=title)

projdir = maindir + title
logsdir = './Logs/'

ag.sort_logs(projdir, logsdir)

ag.fill_spreadsheets(projdir)
```

A basic script for converting all files within a directory into their next calculation type. Also separates the files that GAMESS(us) calculation did not terminate successfully.

```python
import os
import autogamess as ag

idir = './inps/'
ldir = './logs-dats/'
done = './done/'
fail = './failed/'
iext = '.inp'
lext = '.log'
dext = '.dat'

for file in os.listdir(ldir):
    if lext not in file:
        continue

    if '_opt' in file:     
        inp = idir + file.replace(lext, iext)
        dat = ldir + file.replace(lext, dext)
        log = ldir + file
        try:
            ag.opt2hes(inp, log)
        except:
            os.rename(inp, inp.replace(idir, fail))
            os.rename(log, log.replace(ldir, fail))
            os.rename(dat, dat.replace(ldir, fail))
            continue
        os.rename(inp, inp.replace(idir, done))
        os.rename(log, log.replace(ldir, done))
        os.rename(dat, dat.replace(ldir, done))

    if '_hes' in file:
        inp = idir + file.replace(lext, iext)
        dat = ldir + file.replace(lext, dext)
        log = ldir + file
        try:
            ag.hes2raman(inp, dat)
        except:
            os.rename(inp, inp.replace(idir, fail))
            os.rename(log, log.replace(ldir, fail))
            os.rename(dat, dat.replace(ldir, fail))
            continue
        os.rename(inp, inp.replace(idir, done))
        os.rename(log, log.replace(ldir, done))
        os.rename(dat, dat.replace(ldir, done))
```

A less common method of utilizing AutoGAMESS is to parse any single output file for data. The get_data function which is typically meant to be an internally used function can be called by the user. This will retrieve the data from the file, it will read the file name to get the run type.

```python
import autogamess as ag

file = 'AG-test_H2O_B3LYP_CCD_opt.log'

data = ag.get_data(file)

lengths = data.bond_lengths
angles  = data.bond_angles
```
