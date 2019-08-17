from .config import *
from openpyxl import load_workbook

def generate_scaling_factors(projdir, expt_dict, species, method='scott'):
    """
    This function generates scaling factors and scaled frequencies.

    Parameters
    ----------
    projdir: string
        This should be a full directory string pointing to the project
        directory initlly created by new_project.
    expt_dict: dictionary
        This should be a python dictionary with the experimental frequency
        values for all species that the user wants to generate scaling factors
        for in it. Format is explained in Notes section.
    species: list
        This should be a list of all species the user would like scaling factors
        generated for. Any molecule in the list must have experimental data in
        the `expt_dict` associated with it.
    method: string [Optional]
        This should be string giving the method for scaling factor calculation,
        options are `scott`(defualt).

    Notes
    -------
    `expt_dict` format should be as follows:

            {`specie`: [`nu_1`, `nu_2`, ... , `nu_N`]}

     where `specie` must be written the same way as the Excel spreadsheet file
     for that molecule is written. Each frequency, `nu`, should be given in
     the same order as they appear (left to right) in the spreadsheet.

     `species` list format can be in any order but must adhere to the rule
     that any element in `species` is a key for `expt_dict`

     Once execution of this function is completed the `Hessian` worksheet
     will be updated to have a coulmn giving `Scaling Factor/RMS`, as well
     as the scaled frequencies will appear in parathesis next to the predicted
     frequencies. 

    Returns
    -------
    This function returns nothing.

    Example
    -------
    >>> import autogamess as ag
    >>>
    >>> projdir   = './Your Project Title/'
    >>> expt_dict = {'H2O': [1595, 3657, 3756]}
    >>> species   = ['H2O']
    >>>
    >>> ag.generate_scaling_factors(projdir, expt_dict, species)
    >>>
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
