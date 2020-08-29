from pylinac_dev import WinstonLutz
import ConvertToDicom
import pydicom #https://pydicom.github.io/pydicom/stable/tutorials/
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from datetime import datetime
import numpy as np
import glob
import os
import math
import csv

def rename_analized_folder(folder):
    try:
        os.rename(folder,folder + '_analisado')
    except:
        print('Nao foi possivel renomear a pasta ' + file)


def rename_wl(root):
    list_files = glob.glob(root + '/*')
    for file in list_files:
        path,name = os.path.split(os.path.splitext(file)[0])
        if not 'analisado' in name:
            if (name != 'Analises') and (name[-1] != 'r'):
                dia = file[8:10]
                mes = file[10:13]
                ano = file[13:17]
                meses = ['JAN', 'FEV', 'MAR','ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
                meses_dict = {'JAN':'01', 'FEV':'02', 'MAR':'03','ABR':'04', 'MAI':'05', 'JUN':'06', 'JUL':'07', 'AGO':'08', 'SET':'09', 'OUT':'10', 'NOV':'11', 'DEZ':'12'}
                if mes in meses:
                    mes = str(meses_dict[mes])

                file2 = './WL/WL_' + ano + '-' + mes + '-' + dia + '_r'
                try:
                    os.rename(file,file2)
                except:
                    print('Nao foi possivel renomear a pasta ' + file)



#lista_resultado = []
lista_resultado = [['Data', 'Iso Gantry', 'Iso Colimador', 'Iso Gantry e Colimador', 'Iso Mesa',
                   'G0C0T0', 'G90C0T0', 'G180C0T0', 'G0C270T0', 'G270C0T0', 'G0C90T0', 'G0C0T270', 'G0C0T90']]
root = './WL'
rename_wl(root)
root_folders = glob.glob(root + '/*')
#root_folders = ['./WL/WL_20200706']
root_folders.sort()
analisaveis = [str(k) for k in range(1,9)]

try:
    os.mkdir(root + '/Analises')
except:
    print('')
try:
    path_to_jpg_file = root + '/Analises' + '/Resultados_jpg'
    os.mkdir(path_to_jpg_file)
except:
    print('')
try:
    path_to_pdf_file = root + '/Analises' + '/Resultados_pdf'
    os.mkdir(path_to_pdf_file)
except:
    print('')

for folder in root_folders:
    if not 'analisado' in folder:
        list_img_files = glob.glob(folder + '/*.tif')
        path_to_folder,folder_name = os.path.split(os.path.splitext(folder)[0])
        pdf_file = path_to_pdf_file + '/' + folder_name + '.pdf'
        jpg_file = path_to_jpg_file + '/' + folder_name + '.jpg'
        translacao = [0.0, 0.0]
        sad = 1000.0
        sid = 1600.0
        gantry = 0.0
        colimador = 0.0
        mesa = 0.0
        if len(list_img_files)>0:
            path_to_dcm_file = folder + '/WL_dcm'

            meta_data = {'Autor': 'William A. P. dos Santos',
                             'Função': 'Físico',
                             'Acelerador Linear': 'Synergy Full',
                             'Modelo MLC': 'Agility'}
            notes = ['Análise de Winston-Lutz com pylinac',
                     'Campo 2 cm X 2 cm',
                     'Tolerância: 1 mm',
                     'Limite de ação: 0.8 mm',
                     'Local das imagens: ' + folder]

            try:
                os.mkdir(path_to_dcm_file)
            except:
                print('ok')
        for img in list_img_files:
            caminho,nome = os.path.split(os.path.splitext(img)[0])
            tiff_file = caminho + '/' + nome + '.tif'
            if nome[-1] == ' ':
                i = -2
            else:
                i = -1
            if nome[i] == '8':
                dcm_file = path_to_dcm_file + '/' + 'couch90.dcm'
                gantry = 0.0
                colimador = 0.0
                mesa = 90.0
            elif nome[i] == '7':
                dcm_file = path_to_dcm_file + '/' + 'couch270.dcm'
                gantry = 0.0
                colimador = 0.0
                mesa = 270.0
            elif nome[i] == '6':
                dcm_file = path_to_dcm_file + '/' + 'coll90.dcm'
                gantry = 0.0
                colimador = 90.0
            elif nome[i] == '5':
                dcm_file = path_to_dcm_file + '/' + 'gantry270.dcm'
                gantry = 270.0
                colimador = 0.0
            elif nome[i] == '4':
                dcm_file = path_to_dcm_file + '/' + 'coll270.dcm'
                gantry = 0.0
                colimador = 270.0
            elif nome[i] == '3':
                dcm_file = path_to_dcm_file + '/' + 'gantry180.dcm'
                gantry = 180.0
                colimador = 0.0
            elif nome[i] == '2':
                dcm_file = path_to_dcm_file + '/' + 'gantry90.dcm'
                gantry = 90.0
                colimador = 00.0
            else:
                dcm_file = path_to_dcm_file + '/' + 'gantry0.dcm'
                gantry = 0.0
                colimador = 0.0
            if nome[i] in analisaveis:
                ConvertToDicom.convert(nome, nome, tiff_file, dcm_file, translacao, sad, sid, gantry, colimador, mesa=mesa)

        try:
            wl = WinstonLutz(path_to_dcm_file, use_filenames=False)
            #print(wl.results())
            #wl.plot_summary()
            wl.save_summary(jpg_file)
            wl.publish_pdf(filename=pdf_file, notes=notes, open_file=False, metadata=meta_data, customized=True)
            
            gantry_iso_size = wl.gantry_iso_size
            collimator_iso_size = wl.collimator_iso_size
            gantry_coll_iso_size = wl.gantry_coll_iso_size
            couch_iso_size = wl.couch_iso_size
            error_list = {i: 0.0 for i in range(1,9)}
            lin = [folder_name[3:13], f"{gantry_iso_size:2.3f}", f"{gantry_iso_size:2.3f}", f"{gantry_coll_iso_size:2.3f}", f"{couch_iso_size:2.3f}"]
            #print(wl.cax2bb_distance(metric='median'))
            #print(wl.cax2bb_distance(metric='max'))

            axis_list = [('Gantry','Reference'), ('Collimator','Reference'), ('Couch','Reference')]
            for axis in axis_list:
                field_image_list = wl._get_images(axis=axis)
                for field_image in field_image_list[-1]:
                    if (field_image.cax2bb_vector.x**2)>(field_image.cax2bb_vector.y**2):
                        max_num = field_image.cax2bb_vector.x
                    else:
                        max_num = field_image.cax2bb_vector.y
                    if axis[0]=='Gantry':
                        if field_image.gantry_angle==0:
                            error_list[1] = max_num
                        elif field_image.gantry_angle==90:
                            error_list[2] = max_num
                        elif field_image.gantry_angle==180:
                            error_list[3] = max_num
                        elif field_image.gantry_angle==270:
                            error_list[5] = max_num
                    elif axis[0]=='Collimator':
                        if field_image.collimator_angle==90:
                            error_list[6] = max_num
                        elif field_image.collimator_angle==270:
                            error_list[4] = max_num
                    elif axis[0]=='Couch':
                        if field_image.couch_angle==90:
                            error_list[8] = max_num
                        elif field_image.couch_angle==270:
                            error_list[7] = max_num
            for key,value in error_list.items():
                lin.append(f"{value:2.3f}")
            lista_resultado.append(lin)
            os.rename(folder,folder[0:-1] + 'analisado')
        except:
            print(folder + ': Pasta nao possui imagens para analise')

error_file_name = root + '/Analises' + '/Historico_WL.dat'
file_exists = os.path.exists(error_file_name)
with open(root + '/Analises' + '/Historico_WL.dat', 'a', newline='') as error_file:
    df = csv.writer(error_file,delimiter='\t', quotechar='"')
    if file_exists:
        for line in lista_resultado[1:]:
            df.writerow(line)
    else:
        for line in lista_resultado:
            df.writerow(line)

