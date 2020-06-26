from ..config import *

def prep_data(sheetsdir, ref_theory_map, compare_to, savedir=False):
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
    fe = 'Frequency'
    bl = 'Bond Length'
    ir = 'Infrared'
    ra = 'Raman'

    #Other predefined strings
    png      = '.png'
    xlsx     = '.xlsx'
    engine   = 'xlsxwriter'
    X        = 'X'

    #Initialize plot dictionary
    opt_plot_dict  = {}
    freq_plot_dict = {}
    ir_plot_dict   = {}
    ram_plot_dict  = {}

    #Prep non-varied lists to iterate over
    dicts = [opt_plot_dict, freq_plot_dict, ir_plot_dict, ram_plot_dict]
    filts = [bl, fe, ir, ra]

    for file in os.listdir(sheetsdir):

        #Make DataFrame from the excel file
        opt_df = pd.read_excel(sheetsdir + file, index_col=0,
                               sheet_name=opt, header=6)
        hes_df = pd.read_excel(sheetsdir + file, index_col=0,
                               sheet_name=hes, header=6)
        ram_df = pd.read_excel(sheetsdir + file, index_col=0,
                               sheet_name=ram, header=6)

        #Prep DataFrame list for iterating over
        dfs = [opt_df, hes_df, hes_df, ram_df]

        for i in range(len(dicts)):
            df         =   dfs[i]
            regex      = filts[i]
            dicti      = dicts[i]
            ref_theory = ref_theory_map[regex]

            ref_level_str = ref_theory[0] + '/' + ref_theory[1]

            #Pull the subset of the Data Frame that is
            #reference theory level data
            ref_df = df[         df[te] == ref_theory[0] ]
            ref_df = ref_df[ ref_df[bs] == ref_theory[1] ]
            x_vals = ref_df.filter(regex=regex).values.flatten()


            try:
                new_x = np.append(dicti[ref_level_str], x_vals)
                dicti[ref_level_str]  = new_x
            except:
                dicti[ref_level_str]  = x_vals



            for comp_level in compare_to:
                comp_level_str = comp_level[0] + '/' + comp_level[1]

                y_df   = df[     df[te] == comp_level[0] ]
                y_df   = y_df[ y_df[bs] == comp_level[1] ]
                y_vals = y_df.filter(regex=regex).values.flatten()

                if comp_level_str == ref_level_str:
                    continue

                if len(x_vals) != len(y_vals):
                    y_vals = np.empty(len(x_vals))

                try:
                    new_y = np.append(dicti[comp_level_str], y_vals)
                    dicti[comp_level_str]  = new_y
                except:
                    dicti[comp_level_str]  = y_vals

    if savedir:
        #Define header for Spreadsheets
        header = [version, author, '',
                  'Project Name : To Plot',
                  'Molecule Name:  Bunch of them']

        #Define Excell filename
        xlfilename = savedir + 'To_Plot.xlsx'

        #Initialize writer
        writer = pd.ExcelWriter(xlfilename, engine=engine)

        for i in range(len(dicts)):
            sheet = filts[i]
            data  = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dicts[i].items()]))

            data.to_excel(writer, startrow=6, startcol=0, sheet_name=sheet)
            worksheet = writer.sheets[sheet]

            #Write Header
            for line in header:
                i = header.index(line)
                worksheet.write(i, 0, line)

            #Write Units in header
            u  = 'Units:'
            bl = 'Bond Length (Å)'
            vf = 'Vibrational Frequency (cm⁻¹)'
            ii = 'Infrared Intensity (km mol⁻¹)'
            ra = 'Raman Activity (angstrom⁴ amu⁻¹)'
            fv = 'VSCF Frequency (cm⁻¹)'
            iv = 'VSCF IR (km mol⁻¹)'
            hf = 'Heat of Formation (kcal mol⁻¹)'
            sb = '          '
            if sheet == 'Bond Length':
                worksheet.write(2, 0, u + sb + bl)
            if sheet == 'Frequency':
                worksheet.write(2, 0, u + sb + vf)
            if sheet == 'Infrared':
                worksheet.write(2, 0, u + sb + ii)
            if sheet == 'Raman':
                worksheet.write(2, 0, u + sb + ra)

        #Save Excell file
        writer.save()
        return pd.read_excel(xlfilename, index_col=0, header=6)
    else:
        full_data = {}
        for i in range(len(dicts)):
            name  = filts[i]
            data  = pd.DataFrame(dicts[i])

            full_data[name] = data

        return pd.DataFrame(full_data)
