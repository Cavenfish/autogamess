from autogamess import os
from ..setup    import version

def input_builder(txtfile):
    """
    This function build optimization input files.
    """

    with open(txtfile, "r") as f:
        stuff = f.readlines()
        s     = stuff.index("Species\n")
        t     = stuff.index("Theory\n")
        b     = stuff.index("Bassis\n")
        eB    = stuff.index("External Bassis Sets\n")
        i     = stuff.index("Basic Input\n")
        e     = stuff.index("END\n")
        species = stuff[s+1:t:1]
        theories = stuff[t+1:stuff.index("Input Style\n"):1]
        bassis = stuff[b+1:eB:1]
        eBassis = stuff[eB+1:i:1]
        tIn = stuff[stuff.index("Input Style\n") + 1:b:1]

    f.close()

    myFile = []
    for specie in species:
        for theorie in theories:
            for eBassi in eBassis:
                myFile.append( ibv+'_' + specie.strip('\n') + '_' +
                               theorie.strip('\n') + '_' +
                               eBassi.strip('\n') + "_opt.inp" )
            for bassi in bassis:
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
        for bassi in bassis:
            if '_'+bassi.strip('\n')+'_' in filename:
                if "G-" in bassi:
                    bIn = bassi.split("-")
                    if bIn[2].count('p') == 1:
                        f.write(stuff[e-3].replace("bassis", 'N' + bIn[1]
                                                   + " NGAUSS=" + bIn[0]
                                                   + " NDFUNC=" + bIn[3][0]
                                                   + " NPFUNC=" + bIn[4][0] + '\n'
                                                   + " DIFFSP=.TRUE."))

                    if bIn[2].count('p') == 2:
                        f.write(stuff[e-3].replace("bassis", 'N' + bIn[1]
                                                   + " NGAUSS=" + bIn[0]
                                                   + " NDFUNC=" + bIn[3][0]
                                                   + " NPFUNC=" + bIn[4][0] + '\n'
                                                   + " DIFFS=.TRUE."
                                                   + " DIFFSP=.TRUE."))

                    if bIn[2].count('p') == 0:
                        f.write(stuff[e-3].replace("bassis", 'N' + bIn[1]
                                                   + " NGAUSS=" + bIn[0]
                                                   + " NDFUNC=" + bIn[3][0]
                                                   + " NPFUNC=" + bIn[4][0]))
                else:
                    f.write(stuff[e-3].replace("bassis", bassi.strip('\n')))
        if "CCSD(T)" in filename:
            f.write(" $CCINP MAXCC=100 MAXCCL=100 $END\n")
        f.writelines(stuff[e-2:e:1])
        f.close()


    with open("Text Files/InitialCoordinates.txt", "r") as f:
        coords = f.readlines()

    f.close()


    meuFile = []
    with open("Text Files/External Bassis File Names.txt", "r") as f:
        for line in f:
            meuFile.append(line)

    f.close()


    for filename in myFile:
        for eBassi in eBassis:
            if '_'+eBassi.strip('\n')+'_' in filename:
                for specie in species:
                    if '_'+specie.strip('\n')+'_' in filename:
                        for filenome in meuFile:
                            if eBassi.strip('\n')+'_' in filenome:
                                f = open(version+'/'+filename, "a")
                                f1 = open("Text Files/Bassis Sets/"+filenome.strip('\n'), "r")
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
        for bassi in bassis:
            if '_'+bassi.strip('\n')+'_' in filename:
                for specie in species:
                    if '_'+specie.strip('\n')+'_' in filename:
                        f = open(version+'/'+filename, "a")
                        f.writelines(coords[coords.index(specie)+ 1
                                            :coords.index(specie.strip('\n')+" F\n")
                                            :1])
                        f.close()




    with open("Optimization.bat", "w") as f:
        for filename in myFile:
            if "H2O" in filename:
                if ("MP2_CC5" in filename) or ("MP2_CC6" in filename) or ("MP2_PCseg-4" in filename):
                    f.write("call rungms " + filename
                            + " 2018-R1-pgi-mkl 1 0 "
                            + "Optimization_Log_Folder/"+filename.replace(".inp", ".log")
                            + '\n')
                    f.write("PING -n 10 127.0.0.1 > NUL\n")
                    f.write("\n")

                else:
                    f.write("call rungms " + filename
                            + " 2018-R1-pgi-mkl 4 0 "
                            + "Optimization_Log_Folder/"+filename.replace(".inp", ".log")
                            + '\n')
                    f.write("PING -n 10 127.0.0.1 > NUL\n")
                    f.write("\n")

            elif ("MP2_CC5" in filename) or ("MP2_CC6" in filename) or ("MP2_PCseg-4" in filename):
                f.write("call rungms " + filename
                        + " 2018-R1-pgi-mkl 1 0 "
                        + "Optimization_Log_Folder/"+filename.replace(".inp", ".log")
                        + '\n')
                f.write("PING -n 10 127.0.0.1 > NUL\n")
                f.write("\n")

            else:
                f.write("call rungms " + filename
                        + " 2018-R1-pgi-mkl 6 0 "
                        + "Optimization_Log_Folder/"+filename.replace(".inp", ".log")
                        + '\n')
                f.write("PING -n 10 127.0.0.1 > NUL\n")
                f.write("\n")

    f.close()





    for specie in species:
        with open("Spreadsheets/Opt "+specie.strip('\n')+".csv", "w") as f:
            f.write("Molecule: "+specie.strip('\n')+",\n")
            f.write(",,,OPTIMIZATION,\n")
            for theorie in theories:
                f.write("\n\n")
                f.write("Theory: "+theorie.strip('\n')+",\n\n")
                f.write(",Basis,,,Time,,CPU PCT,,Bond,\n")
                for bassi in bassis:
                    f.write(theorie.strip('\n')+','+bassi.strip('\n')+",,,insertTime,,insertCPUPCT,,insertBonds,\n")
                for eBassi in eBassis:
                    f.write(theorie.strip('\n')+','+eBassi.strip('\n')+",,,insertTime,,insertCPUPCT,,insertBonds,\n")

        with open("Spreadsheets/Hes "+specie.strip('\n')+".csv", "w") as f:
            f.write("Molecule: "+specie.strip('\n')+",\n")
            f.write(",,,HESSIAN,\n")
            for theorie in theories:
                f.write("\n\n")
                f.write("Theory: "+theorie.strip('\n')+",\n\n")
                f.write(",Basis,,,Time,,CPU PCT,,Bond,\n")
                for bassi in bassis:
                    f.write(theorie.strip('\n')+','+bassi.strip('\n')+",,,insertTime,,insertCPUPCT,,insertBonds,\n")
                for eBassi in eBassis:
                    f.write(theorie.strip('\n')+','+eBassi.strip('\n')+",,,insertTime,,insertCPUPCT,,insertBonds,\n")

        with open("Spreadsheets/Raman "+specie.strip('\n')+".csv", "w") as f:
            f.write("Molecule: "+specie.strip('\n')+",\n")
            f.write(",,,RAMAN,\n")
            for theorie in theories:
                f.write("\n\n")
                f.write("Theory: "+theorie.strip('\n')+",\n\n")
                f.write(",Basis,,,Time,,CPU PCT,,Bond,\n")
                for bassi in bassis:
                    f.write(theorie.strip('\n')+','+bassi.strip('\n')+",,,insertTime,,insertCPUPCT,,insertBonds,\n")
                for eBassi in eBassis:
                    f.write(theorie.strip('\n')+','+eBassi.strip('\n')+",,,insertTime,,insertCPUPCT,,insertBonds,\n")



    f.close()
