from .config   import *
from .get_data import *

def fill_spreadsheets(projdir):
    """
    """
    #Defining directory names
    sorteddir      = projdir + 'Logs/Sorted/'
    sheetsdir      = projdir + 'Spreadsheets/'

    #Define Sheet names
    opt = 'Optimization'
    hes = 'Hessian'
    ram = 'Raman'

    #Define Data Column names
    rt = 'Run Time'
    bs = 'Basis Set'
    cp = 'CPU Percentage'
    te = 'Theory'


    for dir in os.listdir(sorteddir):
        df = pd.read_excel(sheetsdir + dir + '.xlsx', index_col=0,
                           sheet_name=None, header=4)

        for file in os.listdir(sorteddir + dir):
            if '.log' not in file:
                continue
            filename = sorteddir + dir + '/' + file
            theo = file.split('_')[2]
            bset = file.split('_')[3]

            if '_opt' in file:
                temp = df[opt]

                if rt not in df[opt]:
                    df[opt][rt] = np.nan
                if cp not in df[opt]:
                    df[opt][cp] = np.nan

                lengths, angles, tdata = optimization(filename)

                temp=temp.loc[temp[te]==theo]
                temp=temp.loc[temp[bs]==bset]

                for l in lengths:
                    bl = l.split(':')[0] + ' Bond Length'
                    if bl not in df[opt]:
                        df[opt][bl] = np.nan
                    temp[bl] = l.split(':')[1]
                    df[opt].update(temp)

                for a in angles:
                    al = a.split(':')[0] + ' Bond Anlge'
                    if al not in df[opt]:
                        df[opt][al] = np.nan
                    temp[al] = a.split(':')[1]
                    df[opt].update(temp)

                temp[rt] = tdata[0]
                temp[cp] = tdata[1]

                df[opt].update(temp)


            if '_hes' in file:
                temp = df[hes]

                if rt not in df[hes]:
                    df[hes][rt] = np.nan
                if cp not in df[hes]:
                    df[hes][cp] = np.nan

                data, time, cpu = hessian(filename)

                temp=temp.loc[temp[te]==theo]
                temp=temp.loc[temp[bs]==bset]

                for vib in data[1:-1]:
                    vi = (vib.split()[0] + '(' + vib.split()[2] + ')' +
                          ' Vibrational Frequency')
                    if vi not in df[hes]:
                        df[hes][vi] = np.nan
                    temp[vi] = vib.split()[1]
                    df[hes].update(temp)

                for vib in data[1:-1]:
                    vi = (vib.split()[0] + '(' + vib.split()[2] + ')' +
                          ' Infrared Intensity')
                    if vi not in df[hes]:
                        df[hes][vi] = np.nan
                    temp[vi] = vib.split()[4]
                    df[hes].update(temp)

                temp[rt] = time
                temp[cp] = cpu

                df[hes].update(temp)

            if '_raman' in file:
                temp = df[ram]

                if rt not in df[ram]:
                    df[ram][rt] = np.nan
                if cp not in df[ram]:
                    df[ram][cp] = np.nan

                data, time, cpu = raman(filename)

                temp=temp.loc[temp[te]==theo]
                temp=temp.loc[temp[bs]==bset]

                for vib in data[1:-1]:
                    vi = (vib.split()[0] + '(' + vib.split()[2] + ')' +
                          ' Vibrational Frequency')
                    if vi not in df[ram]:
                        df[ram][vi] = np.nan
                    temp[vi] = vib.split()[1]
                    df[ram].update(temp)

                for vib in data[1:-1]:
                    vi = (vib.split()[0] + '(' + vib.split()[2] + ')' +
                          ' Infrared Intensity')
                    if vi not in df[ram]:
                        df[ram][vi] = np.nan
                    temp[vi] = vib.split()[4]
                    df[ram].update(temp)

                for vib in data[1:-1]:
                    vi = (vib.split()[0] + '(' + vib.split()[2] + ')' +
                          ' Raman Activity')
                    if vi not in df[ram]:
                        df[ram][vi] = np.nan
                    temp[vi] = vib.split()[5]
                    df[ram].update(temp)

                temp[rt] = time
                temp[cp] = cpu

                df[ram].update(temp)

        with pd.ExcelWriter(sheetsdir + dir + '.xlsx') as writer:
            df[opt].to_excel(writer, sheet_name=opt, startrow=4)
            df[hes].to_excel(writer, sheet_name=hes, startrow=4)
            df[ram].to_excel(writer, sheet_name=ram, startrow=4)
