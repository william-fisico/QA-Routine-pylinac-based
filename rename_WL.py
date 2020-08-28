import os
import glob

list_files = glob.glob('./WL/*')
for file in list_files:
    dia = file[8:10]
    mes = file[10:13]
    ano = file[13:17]
    meses = ['JAN', 'FEV', 'MAR','ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    meses_dict = {'JAN':'01', 'FEV':'02', 'MAR':'03','ABR':'04', 'MAI':'05', 'JUN':'06', 'JUL':'07', 'AGO':'08', 'SET':'09', 'OUT':'10', 'NOV':'11', 'DEZ':'12'}
    if mes in meses:
        mes = str(meses_dict[mes])

    file2 = './WL/WL_' + ano + mes + dia
    print(file2)
    os.rename(file,file2)

