from ..config import *
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def make_scatter(data, savedir):
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
    markers  = ['x', '<', '>', 's', 'o', 'd', '*', '$\odot$', '$\dagger$',
                '$\oplus$', '$\circledcirc$', '$\oslash$',
                '$\ltimes$']
    colors   = ['r','k','blue','darkorange', 'lime','olive', 'deepskyblue',
                'purple', 'gold']


    if xlsx in data:
        data = pd.read_excel(data,  index_col=0, sheet_name=None, header=6)

    for name, df in data.items():
        ref = df.columns[0]

        for col in df:
            dir_path = savedir + name + '/' + col.replace('/', '_') + '/'

            try:
                os.makedirs(dir_path)
            except:
                pass

            x   = df[ref]
            y   = df[col]
            l   = np.arange(min(x), max(x), (max(x) - min(x))/100)
            try:
                t,p = ttest_ind(x, y, equal_var=False, nan_policy='omit')
                s   = 't = ' + str(round(t, 3)) + '\np = ' + str(round(p, 3))
            except:
                s   = ''

#--------------------Original Plot----------------------------------
            fig, ax = plt.subplots()
            plt.scatter(x, y, marker='x', color='red', label=col)
            plt.plot(l, l, color='black', linewidth=0.75, label=None)
            if s:
                txt = plt.text(0.05, 0.85, s, transform=ax.transAxes)
            plt.legend()
            plt.tight_layout()
            plt.savefig(dir_path + 'Linear.png')
            if 'Bond' in name:
                plt.close()
            else:
                plt.loglog()
                plt.savefig(dir_path + 'LogLog.png')
                plt.close()
#--------------------Original Plot----------------------------------


#--------------------Difference Plot----------------------------------
            plt.scatter(x, y-x, marker='x', color='red', label=col)
            plt.plot(l, l-l, color='black', linewidth=0.75, label=None)
            plt.legend()
            plt.tight_layout()
            plt.savefig(dir_path + 'Linear--Dif.png')
            if 'Bond' in name:
                plt.close()
            else:
                plt.loglog()
                plt.savefig(dir_path + 'LogLog--Dif.png')
                plt.close()
#--------------------Difference Plot----------------------------------

    return
