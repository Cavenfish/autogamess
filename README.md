# AutoGAMESS

This is a python module for automating Raman calculations using the GAMESS(us) Quantum Chemistry software.

# Installing AutoGAMESS

AutoGAMESS can be installed using

`py -m pip install autogamess --user`

# Input Descriptions
All user functions contian doc strings with examples and explanations of parameters and returns. However, a few functions require specific inputs not fully explained in the doc strings. Such as the functions:
* new_project
* input_builder

The CSV file rquired by both functions must have the following format. The first line must be the header, written exactly as follows.

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

initial_coords_dict is another input parameter that requires specific formatting. The dictioanry is meant to give the intial guess coordinates for a particular symmetry of a molecule. This should be a python dictionary that has the Species (molecule) name as the key and a list with the following format.

`key = 'H2O'`

`value = ['CnV 2,\n','\n',
' O           8.0  -0.0000000000   0.0000000000  -0.0123155409\n',
' H           1.0  -0.0000000000  -0.7568005555   0.5926935705\n']`

`initial_coords_dict = {key : value}`

Some molecules are already compiled within AutoGAMESS default dictionary however, if one of the molecules in the input CSV file is not within the default dictionary a complete dictionary with all molecules within the CSV file is required by AutoGAMESS. 
