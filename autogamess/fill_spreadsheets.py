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

    for dir in os.listdir(sorteddir):
        df = pd.read_excel(sheetsdir + dir + '.xlsx', index_col=0,
                           sheet_name=None, header=4)

        for file in os.listdir(sorteddir + dir):
            filename = sorteddir + dir + '/' + file
            theo = file.split('_')[2]
            bset = file.split('_')[3]

            if '_opt' in file:
                temp = df[opt]

                if rt not in df[opt]:
                    df[opt][rt] = np.nan
                if cp not in df:
                    df[opt][cp] = np.nan

                length, angle, tdata = optimization(filename)

                temp=temp.loc[theo]
                temp=temp.loc[temp[bs]==bset]

                temp[rt] = tdata[0]
                temp[cp] = tdata[1]

                df[opt].update(temp)


            if '_hes' in file:
                df = pd.read_excel(sheetsdir + dir + '.xlsx',
                                    sheet_name='Hessian', header=4)
                data0, data1 = hessian(filename)
                df[rt].loc[theo, df[bs]==bset] = data1[0]
                df[cp].loc[theo, df[bs]==bset] = data1[1]

            if '_raman' in file:
                df = pd.read_excel(sheetsdir + dir + '.xlsx',
                                    sheet_name='Raman', header=4)
                data0, data1 = raman(filename)

        with pd.ExcelWriter(sheetsdir + dir + '.xlsx') as writer:
            df[opt].to_excel(writer, sheet_name=opt, startrow=4)
            df[hes].to_excel(writer, sheet_name=hes, startrow=4)
            df[ram].to_excel(writer, sheet_name=ram, startrow=4)
