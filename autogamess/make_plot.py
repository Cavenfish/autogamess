from .config import *
from .get_data import get_data
from .data_finder import hessian
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def make_plot(file, savedir=None, cmap=['b', 'k', 'r', 'g', 'y', 'c'],
              method=None, sig=300, flag=[]):
    """
    This function make vibrational frequency vs. IR/Raman intensity line plots.

    Parameters
    ----------
    file: string
        This should be a string that points to the log file of a hessian or
        Raman GAMESS(us) calculation. (FULL DIRECTORY STRING REQUIRED)
    savedir: string
        This should be a string that points to the directory in which you
        would like to save the png of the plot.(FULL DIRECTORY STRING REQUIRED)
    cmap: list [Optional]
        This should be a list of Matplotlib allowed color choices. Each symmetry
        will be plotted with a different color in the list.
    method: string [Optional]
        This should be string giving the method for line broadening, options are
        `Gaussian`, `Lorentzian`, None(defualt).
    sig: integer or float [Optional]
        This should be a numerical value to be used as the FWHM for the line
        broadening method chosen. Default: 300 wavenumbers
    flag: list [Optional]
        This should be a list of integers, in particular 1,2 and 3. This list
        tells the function what to plot and what to omit from the plot.
        Please see the Notes section for more details.

    Notes
    -------
    The `flag` parameter is used as follows:

    [Default] `flag=[]`    ---> All lines are plotted
              `flag=[1]`   ---> Vertical lines are not plotted
              `flag=[2]`   ---> Spectral line not plotted
              `flag=[3]`   ---> Gaussian/Lorentzian lines not plotted
              `flag=[1,2]` --->V Vertical lines and Spectral line not plotted

    List combination follow the same format, all possible list combinations
    are allowed.

    Returns
    -------
    This function returns nothing.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> file    = './AGv0-0-6_NH3_CCSD-T_CC6_hes.log'
    >>> savedir = './'
    >>>
    >>> ag.make_plot(file, savedir)
    >>>
    >>> cmap = ['b', 'r', 'k', 'c']
    >>> ag.make_plot(file, savedir, cmap=cmap)
    >>>
    >>> method = 'Lorentzian'
    >>> sig    = 450
    >>>
    >>> ag.make_plot(file, savedir, cmap=cmap, method=method, sig=sig)
    >>>
    """
    #variables declarations
    png  = '.png'

    #get data from file
    data  = get_data(file)

    #If hessian file, make Ir vs Vib Freq plot
    if '_hes' in file:
        ir = data.ir_inten
        vf = data.vib_freq

        #init plot plane
        fig, ax = plt.subplots()

        #get x max
        x_max = 0
        for key in vf:
            x = np.float_(vf[key])
            if max(x) > x_max:
                x_max = max(x)

        #iterate through data making lines
        i    = 0
        x2   = np.arange(0, x_max*1.25, 0.01)
        sum  = np.zeros(len(x2))
        for key in vf:
            x = np.float_(vf[key])
            y = np.float_(ir[key])

            #check flag, plot v lines
            if 1 not in flag:
                ax.vlines(x, 0, y, label=key, colors=cmap[i])
            if (1 in flag) and (3 not in flag):
                ax.vlines(0, 0, 0, label=key, linestyle='--', colors=cmap[i])

            #Make Gaussian line broadening
            if method is 'Gaussian':
                for a,b in zip(x,y):
                    gfit = gaussian(x2, a, sig, b)
                    sum += gfit

                    #Check flag, plot fits
                    if 3 not in flag:
                        ax.plot(x2, gfit, linestyle='--', color=cmap[i])

            #Make Lorentzian line broadening
            if method is 'Lorentzian':
                for a,b in zip(x,y):
                    lfit = lorentzian(x2, a, sig, b)
                    sum += lfit

                    #Check flag, plot fits
                    if 3 not in flag:
                        ax.plot(x2, lfit, linestyle='--', color=cmap[i])

            i += 1

        #check flag, plot fit sum
        if (2 not in flag) and (method is not None):
            ax.plot(x2, sum, alpha=0.5, color='r', label='Spectral Line')

        #init strings
        a     = file.split('_')
        title = a[1] + '(' + a[2] + '/' + a[3] + ')'
        fname = file.split('/')[-1]
        name  = fname.replace('_hes.log', '_ir-plot')

        #Add titles to plot then save
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.legend(loc='upper left')
        plt.xlabel(r'Vibrational Frequency $(cm^{-1})$')
        plt.ylabel(r'Infrared Intensity $(Debye^2 \cdot \AA^{-2} \cdot amu^{-\frac{1}{2}})$')
        plt.title(title, fontsize=20)
        plt.tight_layout()
        if savedir is None:
            plt.show()
        else:
            plt.savefig(savedir + name + png)

    #If raman file, make Raman vs Vib Freq plot
    if '_raman' in file:
        ra = data.raman
        vf = hessian(file)[0]

        #init plot plane
        fig, ax = plt.subplots()

        #get x max
        x_max = 0
        for key in vf:
            x = np.float_(vf[key])
            if max(x) > x_max:
                x_max = max(x)

        #iterate through data making lines
        i = 0
        x2   = np.arange(0, x_max*1.25, 0.01)
        sum  = np.zeros(len(x2))
        for key in vf:
            x = np.float_(vf[key])
            y = np.float_(ra[key])

            #check flag, plot v lines
            if 1 not in flag:
                ax.vlines(x, 0, y, label=key, colors=cmap[i])
            if (1 in flag) and (3 not in flag):
                ax.vlines(0, 0, 0, label=key, linestyle='--', colors=cmap[i])

            #Make Gaussian line broadening
            if method is 'Gaussian':
                for a,b in zip(x,y):
                    gfit = gaussian(x2, a, sig, b)
                    sum += gfit

                    #Check flag, plot fits
                    if 3 not in flag:
                        ax.plot(x2, gfit, linestyle='--', color=cmap[i])

            #Make Lorentzian line broadening
            if method is 'Lorentzian':
                for a,b in zip(x,y):
                    lfit = lorentzian(x2, a, sig, b)
                    sum += lfit

                    #Check flag, plot fits
                    if 3 not in flag:
                        ax.plot(x2, lfit, linestyle='--', color=cmap[i])

            i += 1

        #check flag, plot fit sum
        if (2 not in flag) and (method is not None):
            ax.plot(x2, sum, alpha=0.5, color='r', label='Spectral Line')

        #init strings
        a     = file.split('_')
        title = a[1] + '(' + a[2] + '/' + a[3] + ')'
        fname = file.split('/')[-1]
        name  = fname.replace('_raman.log', '_raman-plot')

        #Add titles to plot then save
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.legend(loc='upper left')
        plt.xlabel(r'Vibrational Frequency $(cm^{-1})$')
        plt.ylabel(r'Raman Intensity $(\AA^{4}\cdot mol^{-1})$')
        plt.title(title, fontsize=20)
        plt.tight_layout()
        if savedir is None:
            plt.show()
        else:
            plt.savefig(savedir + name + png)

    return
