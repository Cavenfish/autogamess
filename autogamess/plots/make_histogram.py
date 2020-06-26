from ..config import *
import matplotlib.pyplot as plt

def make_histogram(sheetsdir, ref_theory, savedir):
    """
    sheetsdir: string
        This should be a full directory string pointing to the spreadsheets
        directory.

    savedir: string
        This should be a string that points to the directory in which you
        would like to save the png of the plot.(FULL DIRECTORY STRING REQUIRED)
    """
    #Define Sheet names
    opt = 'Optimization'
    hes = 'Hessian'
    ram = 'Raman'
    vsc = 'VSCF'

    #Define Data Column names
    rt = 'Run Time'
    bs = 'Basis Set'
    cp = 'CPU Percentage'
    te = 'Theory'
    me = 'Method'

    #Other predefined strings
    xlsx = '.xlsx'
    engine   = 'xlsxwriter'

    #Create a DataFrame for storing the plottable data
    to_plot = pd.DataFrame()

    #iterate through files in sheetsdir
    for file in os.listdir(sheetsdir):

        #Make DataFrame from the excel file
        df = pd.read_excel(sheetsdir + file, index_col=0,
                           sheet_name=opt, header=6)

        #Pull the subset of the Data Frame that is
        #reference theory level data
        ref_df = df[ df[te] == ref_theory[0] ]
        ref_df = ref_df[ ref_df[bs] == ref_theory[1] ]

        #dummy DataFram for holding subrated data
        dum = df.copy()

        #iterate through DataFrame rows
        #Note ->j<- is the row in pandas series format
        #Note ->i<- is the index of the row
        for i,j in df.iterrows():

            #pull out the current row from the DataFrame
            #note, it is pulled out in DataFrame format
            data = df.loc[i:i]

            #pull out the reference theory data in Series format
            x   = ref_df.index[0]
            ref = ref_df.loc[x]

            #Subtracts the reference theory data from the current row
            #Note this only performes the subtration on frequencies
            tmp = data.filter(regex='Length') - ref.filter(regex='Length')
            dum.update(tmp)

        #This puts the DataFrame in a better format for plotting
        dum = dum.set_index(te).transpose().filter(regex='Length', axis=0)

        #This updates the plotting DataFrame
        to_plot = to_plot.append(dum)

    to_plot.dropna(thresh=6, axis='columns', inplace=True)
    writer = pd.ExcelWriter('../../to_plot3.xlsx', engine=engine)
    to_plot.to_excel(writer, startrow=0, startcol=0)
    writer.save()
    #This will take a DataFrame with data in the normal format from
    #AutoGAMESS and plot a histogram of the data with theory levels
    #as the labels (exactly as wanted)
    """
    to_plot.dropna(thresh=5,axis='columns').plot.kde()
    plt.tight_layout()
    plt.savefig(savedir+'test.png')
    plt.close()

    #ax=plt.figure()
    for label, sub_df in to_plot.transpose().groupby(te):
        sub_df.dropna(thresh=5, inplace=True)
        x = sub_df.values.astype(np.float64)
        try:
            plt.kde()
        except:
            ax = plt.kde()
    plt.tight_layout()
    plt.savefig(savedir+'test2.png')
    plt.close()
    """
