from .config import *
from .get_data import get_data
from .data_finder import hessian
import matplotlib.pyplot as plt

def make_plot(file, savedir):
    """
    """
    #variables declarations
    png  = '.png'
    cmap = ['b', 'k', 'r', 'g', 'y', 'c']

    #get data from file
    data  = get_data(file)


    #If hessian file, make Ir vs Vib Freq plot
    if '_hes' in file:
        ir = data.ir_inten
        vf = data.vib_freq

        #init plot plane
        fig, ax = plt.subplots()

        #iterate through data making lines
        i = 0
        for key in vf:
            x = np.float_(vf[key])
            y = np.float_(ir[key])
            ax.vlines(x, 0, y, label=key, colors=cmap[i])
            i += 1

        #init strings
        a     = file.split('_')
        title = a[1] + '(' + a[2] + '/' + a[3] + ')'
        fname = file.split('/')[-1]
        name  = fname.replace('_hes', '_ir-plot')

        #Add titles to plot then save
        plt.ylim(bottom=0)
        plt.legend(loc='upper left')
        plt.xlabel(r'Vibrational Frequency $(cm^{-1})$')
        plt.ylabel(r'Infrared Intensity $(Debey^2 \cdot \AA^{-2} \cdot amu^{-\frac{1}{2}})$')
        plt.title(title, fontsize=20)
        plt.savefig(savedir + name + png)

    #If raman file, make Raman vs Vib Freq plot
    if '_raman' in file:
        ra = data.raman
        vf = hessian(file)[0]

        #init plot plane
        fig, ax = plt.subplots()

        #iterate through data making lines
        i = 0
        for key in vf:
            x = np.float_(vf[key])
            y = np.float_(ra[key])
            ax.vlines(x, 0, y, label=key, colors=cmap[i])
            i += 1

        #init strings
        a     = file.split('_')
        title = a[1] + '(' + a[2] + '/' + a[3] + ')'
        fname = file.split('/')[-1]
        name  = fname.replace('_raman', '_raman-plot')

        #Add titles to plot then save
        plt.ylim(bottom=0)
        plt.legend(loc='upper left')
        plt.xlabel(r'Vibrational Frequency $(cm^{-1})$')
        plt.ylabel(r'Raman Intensity $(\AA^{4}\cdot mol^{-1})$')
        plt.title(title, fontsize=20)
        plt.savefig(savedir + name + png)

    return
