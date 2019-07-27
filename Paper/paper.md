---
title: 'AutoGAMESS: A Python package for automation of GAMESS(us) Raman calculations'
tags:
  - Python
  - computational chemistry
  - automation
  - raman
  - molecular properties
author: |
 | Brian C. Ferrari
 | Department of Physics, University of Central Florida, 4111 Libra Drive, Orlando FL 32816
orcid: 0000-0002-7416-8629
geometry: margin=1in
date: 27 May 2019
bibliography: paper.bib
---

# Summary

The *ab initio* Quantum Chemistry software GAMESS(us)[@schmidt1993general] is capable of calculating a variety of molecular
properties. The software is widely used by chemists, physicists, astro-chemists and astro-physicists
[@burda2004theoretical; @pacifici2013high; @hickman2005dissociative; @bennett2014experimental], for predicting properties of
volatile and unstable species that have not been experimentally characterized or quantized before. Making GAMESS(us) of high
importance to these research groups, because of this large importance numerous third-party softwares have been written to compliment GAMESS(us)
[@schaftenaar2000molden; @schmidt2013webmo; @bode1998macmolplt; @allouche2011gabedit; @dermardirossian2005gdis]. However,
these softwares are largely visualization and graphical softwares, there still is no open-source software for automation
of *ab initio* calculations. Softwares for data collection from the output files of Computation Chemistry softwares have been made[@o2008cclib], but automation of input generation is not included. Research utilizing
*ab initio* calculations typically require calculations with multiple steps for each final result, for instance a raman activity prediction first requires
an optimization and hessian calculation be performed on the molecule, making automation extremely beneficial. Often times single calculations of molecular properties are not reliable resulting is publications requiring several calculations for each property be done on each molecule. As it stands the automation of these calculations is either not being done, or being
implemented individually by each research group utilizing the GAMESS(us) software. This slows scientific progress down, and an automation software written in a language extremely simple and well adopted by scientists, such as Python, is an attractive solution to the problem.
AutoGAMESS is providing an open-source Python based software for automating conversion between Optimization calculations to
Hessian calculations and then to Raman calculations. It also offers automation of data collection from the output files,
for quick tabular data read outs of each calculation.

Functions:

* new_project: Builds a directory tree for housing input/output files with spreadsheets for collected data.
* input_builder: Builds optimization input files based on text file specifications
* opt2hes: Converts optimization input files into hessian input files
* hes2raman: Converts hessians input files into raman input files
* sort_logs: Sorts GAMESS(us) output files
* fill_spreadsheet: Fills in Excel Spreadsheets with data collected from log files
* get_data: Collects data from output files

# Capabilities

AutoGAMESS is capable of initializing an entire directory with well organized subdirectories for housing all input and output files. This main directory will also generate spreadsheets that AutoGAMESS is later capable of filling with the data collected from parsing the output files. Once a main directory is initialized, input files can be generated for GAMESS(us) optimization calculations. Requiring only a simple csv file as input, AutoGAMESS input_builder function can generate thousands of files with any form of internal GAMESS(us) level of theory and both internal and external basis sets.
External basis sets must be a part of ESML Basis Set Exchange [@feller1996role; @schuchardt2007basis], this requirement is due to the integration of the ESML basis set exchange Python package into AutoGAMESS. After the user has run an optimization calculation AutoGAMESS is able to quickly get the required data from the output to modify the optimization input file into a hessian calculation input file. Similarly, after a hessian calculation AutoGAMESS can use the output to quickly generate a raman calculation input file. Once all calculations a user desires to run have been completed AutoGAMESS can sort the output files, then parse files for specific molecular properties and fill in the initially generated spreadsheets. All hessian and raman data is pulled directly from output files, while optimization properties are calculated. Bond lengths are calculated by using the simple Euclidean distance formula

$$ D = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2} $$

While bond angles are calculated using the following equation

$$ A = \arccos{\hat{V_1} \cdot \hat{V_2}} $$

where $\hat{V_1}$ and $\hat{V_2}$ are the normalized vectors for each atoms location in relation to the structures origin.


# Use of AutoGAMESS

AutoGAMESS was developed to be versatile in its usability, however the most
effective method to use AutoGAMESS is the integration of short python scripts
within shell scripts.  

# Availability
This software is distributed under the MIT License and is available from https://github.com/Cavenfish/autogamess
or can be installed through Python's pip install command `py -m pip install autogamess --user`.

# Dependencies

AutoGAMESS requires all the following Python packages:

* NumPy
* SciPy
* Pandas
* basis_set_exchange
* Periodic_Elements
* openpyxl


# Acknowledgements

The author would like to thank Dr. Christopher J. Bennett, Remington Cantelas and Sarah Swiersz for helpful discussions while developing the package.

# References
