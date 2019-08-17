from .config import *
from openpyxl import load_workbook

def generate_scaling_factors(projdir, expt_dict, species, method='nist'):
    """
    """
    #string variables
    sheetsdir      = projdir + 'Spreadsheets/'
    xlsx           = '.xlsx'
    hes            = 'Hessian'

    for specie in species:
        if os.path.isfile(sheetsdir + specie + xlsx):
            df  = pd.read_excel(sheetsdir + specie + xlsx, index_col=0,
                               sheet_name=hes, header=6)
            df2 = pd.read_excel(sheetsdir + specie + xlsx, index_col=0,
                               sheet_name=hes, header=6)

        #get only frequency columns
        x = [col for col in df.columns if 'Vibrational' not in col]
        df.drop(x, axis=1, inplace=True)
        df.dropna(inplace=True)

        #get expt data from dictionary
        expt = expt_dict[specie]

        df2['Scaling Factor/RMS'] = np.nan
        #iterate through DataFrame
        for i,j in df.iterrows():
            theo = list(j.values)

            #get scaling factors
            c, rms = scaling_factor_scott(theo, expt)

            #apply to columns in sliced DataFrame
            df.loc[i] = j.apply(lambda x: str(x) + '(' + str(round(float(x)*c, 2)) + ')')

            #Added column giving Scaling Factor and RMS
            df2.loc[i,'Scaling Factor/RMS'] = str(c) + '/' + str(rms)


        #update main DataFrame
        df2.update(df)

    #write Excel spreadsheet with updated DataFrame
    book = load_workbook(sheetsdir + specie + xlsx)
    with pd.ExcelWriter(sheetsdir + specie + xlsx, engine='openpyxl') as writer:
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        df2.to_excel(writer, sheet_name=hes, startrow=6)

    return
