from ..config import *
import matplotlib.pyplot as plt
from ..dictionaries  import theory_dict

def make_histogram(data, savedir):
    """
    """
    #Define Sheet names
    opt = 'Optimization'
    hes = 'Hessian'
    ram = 'Raman'
    vsc = 'VSCF'

    #Define Data Column names/variables
    rt = 'Run Time'
    bs = 'Basis Set'
    cp = 'CPU Percentage'
    te = 'Theory'
    me = 'Method'
    fe = 'Freq'
    bl = 'Bond Length'
    ir = 'Infrared'
    ra = 'Raman'

    #Other predefined strings
    png      = '.png'
    xlsx     = '.xlsx'
    engine   = 'xlsxwriter'
    X        = 'X'

    #Predefine Markers and Colors
    colors   = ['r','k','blue','darkorange', 'lime','olive', 'deepskyblue',
                'purple', 'gold']


    if xlsx in data:
        data = pd.read_excel(data,  index_col=0, sheet_name=None, header=6)

    for name, df in data.items():
        ref = df.columns[0]
        dir_path = savedir + name + '/'

        try:
            os.makedirs(dir_path)
        except:
            pass

        for col in df:
            if col == ref:
                continue
            x = df[ref]
            y = df[col]
            df[col] = y-x


        df.drop(ref, axis=1, inplace=True)

        df.dropna(thresh=5, axis=1).plot.kde(
        color=('r','k','blue','darkorange', 'lime','olive', 'deepskyblue',
               'purple', 'gold'),
        style=['-', '-', '-', '-', '-', '-', '-', '--', '-'])
        plt.tight_layout()
        plt.savefig(dir_path + 'KDE.png')
        plt.close()

        dft = [k for k,v in theory_dict.items() if 'DFTTYP' in v]
        mp2 = [k for k,v in theory_dict.items() if 'MPLEVL' in v]
        cc  = [k for k,v in theory_dict.items() if 'CCTYP' in v]

        ax = plt.subplot(2,1, 1)
        df.filter(regex=dft).plot.kde(color=colors[mask], ax=ax, sharex=True,
                                      legend=False, style=styles[mask])
        plt.xlim(-0.075,0.075)
        plt.ylabel('')
        #plt.title(r'Vibrational Frequencies Discrepancies', size=18)
        ax = plt.subplot(2,1, 2)
        df.filter(regex=mp2+cc).plot.kde(color=colors[mask], ax=ax, sharex=True,
                                         legend=False, style=styles[mask])
        plt.xlim(-0.075,0.075)
        plt.ylabel('')
        plt.xlabel(r'Predicted Bond Length Difference ($\AA$)', size=15)
        plt.tight_layout()
        plt.savefig('plot_with_subplots-opt.png')
        plt.close()
