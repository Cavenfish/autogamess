call rungms IBv6_H2O_B3LYP_CCD_opt.inp 2018-R1-pgi-mkl 4 0 outputs/IBv6_H2O_B3LYP_CCD_opt.log
PING -n 10 127.0.0.1 > NUL

move ./resart/IBv6_H2O_B3LYP_CCD_opt.dat ./outputs/IBv6_H2O_B3LYP_CCD_opt.dat

python convert_files.py

call rungms IBv6_H2O_B3LYP_CCD_hes.inp 2018-R1-pgi-mkl 4 0 outputs/IBv6_H2O_B3LYP_CCD_hes.log
PING -n 10 127.0.0.1 > NUL

move ./resart/IBv6_H2O_B3LYP_CCD_hes.dat ./outputs/IBv6_H2O_B3LYP_CCD_hes.dat

python convert_files.py

call rungms IBv6_H2O_B3LYP_CCD_raman.inp 2018-R1-pgi-mkl 4 0 outputs/IBv6_H2O_B3LYP_CCD_raman.log
PING -n 10 127.0.0.1 > NUL

python compile_data.py
