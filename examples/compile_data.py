import autogamess as ag

logsdir = './done/'
projdir = './AutoGAMESS COx Project/'

ag.sort_logs(projdir, logsdir)
ag.fill_spreadsheets(projdir)
