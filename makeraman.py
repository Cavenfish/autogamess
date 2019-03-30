import os
import autogamess as ag

inps = './inps/'
rest = './restart/'
hes  = '_hes'
dat  = '.dat'
inp  = '.inp'
check= '_hes.inp'

for filename in os.listdir(inps):
    if check not in filename:
        continue

    hesfile = inps + filename
    datfile = rest + filename.replace(inp, dat)

    if not os.path.isfile(datfile):
        continue

    print(hesfile + "\n")

    ag.hes2raman(hesfile, datfile)
