import os
import autogamess as ag

idir = ''#define here the inputs directory
ldir = ''#define here the outputs directory
done = ''#define here the successfully completed files directory
fail = ''#define here the unsuccessfully completed files directory
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
