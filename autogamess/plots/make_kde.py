from ..config import *
import matplotlib.pyplot as plt
from ..dictionaries  import theory_dict


def make_kde(data, savedir):
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
    styles   = ['-', '-', '-', '-', '-', '-', '-', '--', '-']


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

        df.dropna(thresh=5, axis=1).plot.kde(color=colors, style=styles)
        plt.tight_layout()
        plt.savefig(dir_path + 'KDE.png')
        plt.close()

    return
