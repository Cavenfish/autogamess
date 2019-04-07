import autogamess as ag
import os

logdir = './Sarah_Logs/'

f=open('Sarah_bondData.txt', 'w')

for file in os.listdir(logdir):
    if '_opt' not in file:
        continue

    try:
        lengths, angles, trash = ag.optimization(logdir + file)
    except TypeError:
         continue

    f.write(file + '\n')
    f.write('----Bond Lengths----\n')
    f.writelines(lengths)
    f.write('\n')
    f.write('----Bond Angles----\n')
    f.writelines(angles)
    f.write('\n\n\n')


f.close()
