---
title: 'Autogamess: A Python package for automation of GAMESS(us) molecular properties calculations.'
tags:
  - Python
  - computational chemistry
  - automation
  - raman
  - molecular properties
authors:
  - name: Brian C. Ferrari
	orcid: 0000-0002-7416-8629
    affiliation: 1
affiliations:
 - name: Department of Physics, University of Central Florida, 4111 Libra Drive, Orlando FL 32816
   index: 1
date: 19 May 2019
bibliography: paper.bib
---

# Summary

The **ab initio** Quantum Chemistry software GAMESS(us)[@schmidt1993general] is capable 
calculating a variety of molecular properties. The software is widely used by computational
chemists and astro-chemists [@burda2004theoretical,@pacifici2013high,@hickman2005dissociative,@bennett2014experimental],
because of this large importance numerous third-party softwares have been written to compliment GAMESS(us)
[@schaftenaar2000molden,@schmidt2013webmo,@bode1998macmolplt,@allouche2011gabedit,@dermardirossian2005gdis]. However, 
these softwares are all visualization and graphical softwares, there still is no open-source software for automation
of *ab initio* calculations. As it stands the automation of these calculations is either not being done, or being
implemented individually by each research group utilizing the GAMESS(us) software. Often times research utilizing
*ab initio* calculation require several calcualtions with multi-run steps for each final result, automation is beneficial.
We are providing an open-source Python based software for automating conversion between Optimization calculations to 
Hessian calcualtions and then to Raman calcualtions. We also offer automation of data collection from the output files,
for quick tabular data read outs of each calcualtion. Our hope is to also have this software as a platform for more 
automation programs written by other research groups to be shared with other research groups, helping to expidite 
publications by minimizing software development times for individual groups.

Functions:

* bat_maker: Generates batch files ready for executing GAMES(us) calculations through rungms function.
* new_project: Builds a directory tree for housing input and output files with spreadsheets for housing collected data.
* opt2hes: Converts optimization input files into hessian input files
* sort_logs: Sorts GAMESS(us) output files
* hes2raman: Conversts hessians input files into raman input files
* get_data: Collects data from output files and generates list of data 
* input_builder: Builds optimization input files based on text file specifications 


# Acknowledgements

We acknowledge support from Dr. Christopher J. Bennett, Remington Cantelas, Sarah Swiersz and Nick Brunston during the genesis and testsing of the package.

# References
