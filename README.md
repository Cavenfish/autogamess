# AutoGAMESS

This is a python module for automating Raman calculations using the GAMESS(us) Quantum Chemistry software (https://www.msg.chem.iastate.edu/gamess/).

# Installing AutoGAMESS

AutoGAMESS can be installed using

`pip install autogamess`

# Input Descriptions
All user functions contain doc strings with examples and explanations of parameters and returns. However, a few functions require specific inputs not fully explained in the doc strings. Such as the functions:
* new_project
* input_builder

The CSV file required by both functions must have the following format. The first line must be the header, written exactly as follows.

`Species,Theory,Basis Sets,External Basis Sets,Run Types`

All lines after the header should give input as 1 item per column per line. As shown in the example bellow.

`Species,Theory,Basis Sets,External Basis Sets,Run Types`

`H2O,B3LYP,CCD,Roos-Aug-DZ-ANO,Optimization`

`NH3,MP2,CCT,Roos-Aug-TZ-ANO,Hessian`

`HCN,CCSD-T,CCQ,Sadlej-LPolX-fl,Raman`

`H2CO,,CC5,Sadlej-LPolX-dl,VSCF`

`CH4,,CC6,Sadlej-LPolX-ds`

`C2H6,,ACCD,6-311ppG3df-3pd`

`C2H4,,ACCT,6-311G2df-2pd`

`C2H2,,ACCQ,6-311G2df-2pd`

External basis sets should be written in the same format as they as required by ESML basis_set_exchange (https://github.com/MolSSI-BSE/basis_set_exchange).

initial_coords_dict is another input parameter that requires specific formatting. The dictionary is meant to give the initial guess coordinates for a particular symmetry of a molecule. This should be a python dictionary that has the Species (molecule) name as the key and a list with the following format.

`key = 'H2O'`

`value = ['CnV 2,\n','\n',
' O           8.0  -0.0000000000   0.0000000000  -0.0123155409\n',
' H           1.0  -0.0000000000  -0.7568005555   0.5926935705\n']`

`initial_coords_dict = {key : value}`

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
