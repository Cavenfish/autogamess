from config import *

def convert_ir_units(old, new, sheetsdir):
    """
    """
    #Define Sheet names
    opt = 'Optimization'
    hes = 'Hessian'
    ram = 'Raman'
    vsc = 'VSCF'

    xlsx = '.xlsx'
    CF   = conversion_factor(old, new)

    for file in os.listdir(sheetsdir):

        df = pd.read_excel(sheetsdir + file + xlsx, index_col=0,
                           sheet_name=None, header=6)

        temp = df[hes].filter(regex='Infrared Intensity') * CF
        df[hes].update(temp)

        #Write Spreadsheets
        book = load_workbook(sheetsdir + dir + '.xlsx')
        with pd.ExcelWriter(sheetsdir + dir + '.xlsx', engine='openpyxl') as writer:
            writer.book = book
            writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            if opt in df:
                df[opt].to_excel(writer, sheet_name=opt, startrow=6)
            if hes in df:
                df[hes].to_excel(writer, sheet_name=hes, startrow=6)
            if ram in df:
                df[ram].to_excel(writer, sheet_name=ram, startrow=6)
            if vsc in df:
                df[vsc].to_excel(writer, sheet_name=vsc, startrow=6)


    return
