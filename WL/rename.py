import os
import glob

list_files = glob.glob('*')
for file in list_files:
    file2 = 'WL_' + file[3:12]
    os.rename(file,file2)

