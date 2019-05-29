---
title: 'Autogamess: A Python package for automation of GAMESS(us)'
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
[@burda2004theoretical;@pacifici2013high;@hickman2005dissociative;@bennett2014experimental], for predicting properties of
volatile and unstable species that have not been experimentally characterized or quantized before. Making GAMESS(us) of high
importance to these research groups because of this large importance numerous third-party softwares have been written to compliment GAMESS(us)
[@schaftenaar2000molden;@schmidt2013webmo;@bode1998macmolplt;@allouche2011gabedit;@dermardirossian2005gdis]. However,
these softwares are largely visualization and graphical softwares, there still is no open-source software for automation
of *ab initio* calculations. As it stands the automation of these calculations is either not being done, or being
implemented individually by each research group utilizing the GAMESS(us) software. Often times research utilizing
*ab initio* calculations require several calculations with multiple steps for each final result, for instance a raman activity prediction first requires
an optimization and hessian calculation be performed on the molecule, making automation extremely beneficial.
Autogamess is providing an open-source Python based software for automating conversion between Optimization calculations to
Hessian calculations and then to Raman calculations. It also offers automation of data collection from the output files,
for quick tabular data read outs of each calculation. The hope is to also have this software act as a platform for more
automation programs written by other research groups to be shared with other research groups, helping to expedite
publications by minimizing software development times for individual groups.

Functions:

* new_project: Builds a directory tree for housing input and output files with spreadsheets for housing collected data.
* opt2hes: Converts optimization input files into hessian input files
* sort_logs: Sorts GAMESS(us) output files
* hes2raman: Converts hessians input files into raman input files
* get_data: Collects data from output files and generates list of data
* input_builder: Builds optimization input files based on text file specifications
* fill_spreadsheet: Fills in Excel Spreadsheets with data collected from log files

# Availability 
This software is distributed under the MIT License and is available from https://github.com/Cavenfish/autogamess
or can be installed through Python's pip install command `py -m pip install autogamess --user'.

# Acknowledgements

Thanks to Dr. Christopher J. Bennett, Remington Cantelas, Sarah Swiersz and Nick Brunston for helping to beta test the package.

# References
