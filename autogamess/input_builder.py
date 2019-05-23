from .config import *

def input_builder(txtfile):
    """
    This function build optimization input files.
    """
    ibv     = 'beta'
    version = './test'

    with open(txtfile, "r") as f:
        stuff = f.readlines()
        s     = stuff.index("Species\n")
        t     = stuff.index("Theory\n")
        b     = stuff.index("Basis\n")
        eB    = stuff.index("External Basis Sets\n")
        i     = stuff.index("Basic Input\n")
        e     = stuff.index("END\n")
        species = stuff[s+1:t:1]
        theories = stuff[t+1:stuff.index("Input Style\n"):1]
        basis = stuff[b+1:eB:1]
        ebasis = stuff[eB+1:i:1]
        tIn = stuff[stuff.index("Input Style\n") + 1:b:1]


    myFile = []
    for specie in species:
        for theorie in theories:
            for eBassi in ebasis:
                myFile.append( ibv+'_' + specie.strip('\n') + '_' +
                               theorie.strip('\n') + '_' +
                               eBassi.strip('\n') + "_opt.inp" )
            for bassi in basis:
                myFile.append( ibv+'_' + specie.strip('\n') + '_' +
                               theorie.strip('\n') + '_' +
                               bassi.strip('\n') + "_opt.inp" )





    for filename in myFile:
        f = open(version+'/'+filename, "w")
        f.write('!'+version.replace(',', '.')+'\n')
        f.write("!  by Brian C. Ferrari \n")
        f.write("!\n")
        f.write(stuff[i+1])
        for theorie in theories:
            if theorie.strip('\n')+'_' in filename:
                if (theorie.strip('\n') == "CCSD-T"
                or "CC5_" in filename
                or "CC6_" in filename
                or "PC-seg4_" in filename):
                    f.write(stuff[i+2].replace("theory", tIn[theories.index(theorie)].strip('\n')
                                               +" NUMGRD=.TRUE."))
                else:
                    f.write(stuff[i+2].replace("theory", tIn[theories.index(theorie)].strip('\n')))
        if "6-31" in filename and 'f' not in filename:
            f.write(stuff[i+3].replace("ISPHER=1", "ISPHER=-1"))
        else:
            f.write(stuff[i+3])
        f.writelines(stuff[i+4:e-4:1])
        if "B3LYP" in filename:
            f.write(stuff[e-4])
        for bassi in basis:
            if '_'+bassi.strip('\n')+'_' in filename:
                if "G-" in bassi:
                    bIn = bassi.split("-")
                    if bIn[2].count('p') == 1:
                        f.write(stuff[e-3].replace("basis", 'N' + bIn[1]
                                                   + " NGAUSS=" + bIn[0]
                                                   + " NDFUNC=" + bIn[3][0]
                                                   + " NPFUNC=" + bIn[4][0] + '\n'
                                                   + " DIFFSP=.TRUE."))

                    if bIn[2].count('p') == 2:
                        f.write(stuff[e-3].replace("basis", 'N' + bIn[1]
                                                   + " NGAUSS=" + bIn[0]
                                                   + " NDFUNC=" + bIn[3][0]
                                                   + " NPFUNC=" + bIn[4][0] + '\n'
                                                   + " DIFFS=.TRUE."
                                                   + " DIFFSP=.TRUE."))

                    if bIn[2].count('p') == 0:
                        f.write(stuff[e-3].replace("basis", 'N' + bIn[1]
                                                   + " NGAUSS=" + bIn[0]
                                                   + " NDFUNC=" + bIn[3][0]
                                                   + " NPFUNC=" + bIn[4][0]))
                else:
                    f.write(stuff[e-3].replace("basis", bassi.strip('\n')))
        if "CCSD(T)" in filename:
            f.write(" $CCINP MAXCC=100 MAXCCL=100 $END\n")
        f.writelines(stuff[e-2:e:1])
        f.close()


    with open("./Text Files/InitialCoordinates.txt", "r") as f:
        coords = f.readlines()


    meuFile = []
    with open("./Text Files/External Basis File Names.txt", "r") as f:
        for line in f:
            meuFile.append(line)


    for filename in myFile:
        for eBassi in ebasis:
            if '_'+eBassi.strip('\n')+'_' in filename:
                for specie in species:
                    if '_'+specie.strip('\n')+'_' in filename:
                        for filenome in meuFile:
                            if eBassi.strip('\n')+'_' in filenome:
                                f = open(version+'/'+filename, "a")
                                f1 = open("./Text Files/Basis Sets/"+filenome.strip('\n'), "r")
                                f.writelines(coords[coords.index(specie)+ 1
                                                    :coords.index(specie)+ 3
                                                    :1])
                                things = coords[coords.index(specie)+ 3
                                                :coords.index(specie.strip('\n')+" F\n")
                                                :1]
                                lines = f1.readlines()
                                for thing in things:
                                    if "$END" in thing:
                                        f.write(' '+thing)
                                        f.write('\n')
                                        break
                                    if thing == '\n':
                                        break
                                    f.write(thing)
                                    f.writelines(lines[lines.index(thing[0:10:1]+'\n')+1
                                                       :lines.index(thing[0:10:1] +"F\n")
                                                       :1])
                                    f.write('\n')

                                f.close()
                                f1.close()





    for filename in myFile:
        for bassi in basis:
            if '_'+bassi.strip('\n')+'_' in filename:
                for specie in species:
                    if '_'+specie.strip('\n')+'_' in filename:
                        f = open(version+'/'+filename, "a")
                        f.writelines(coords[coords.index(specie)+ 1
                                            :coords.index(specie.strip('\n')+" F\n")
                                            :1])
                        f.close()


    f.close()
