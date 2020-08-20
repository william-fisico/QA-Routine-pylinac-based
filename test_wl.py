from pylinac_dev import WinstonLutz
import ConvertToDicom
import pydicom #https://pydicom.github.io/pydicom/stable/tutorials/
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import glob
import os

path_to_files = './WL/WL_11AGO2020'
list_img_files = glob.glob(path_to_files + '/*.tif')
translacao = [0.0, 0.0]
sad = 1000.0
sid = 1600.0
gantry = 0.0
colimador = 0.0
x_res = 0.406
path_to_dcm_file = path_to_files + '/WL_dcm'
try:
    os.mkdir(path_to_dcm_file)
except:
    print('ok')
print(list_img_files)
for img in list_img_files:
    caminho,nome = os.path.split(os.path.splitext(img)[0])
    tiff_file = caminho + '/' + nome + '.tif'
    pdf_file = path_to_dcm_file + '/' + nome + '.pdf'
    print(nome[-2])
    if nome[-1] == ' ':
        i = -2
    else:
        i = -1
    if nome[i] == '8':
        dcm_file = path_to_dcm_file + '/' + 'couch90.dcm'
        gantry = 0.0
        colimador = 0.0
    elif nome[i] == '7':
        dcm_file = path_to_dcm_file + '/' + 'couch270.dcm'
        gantry = 0.0
        colimador = 0.0
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
    print(dcm_file)
    ConvertToDicom.convert(nome, nome, tiff_file, dcm_file, translacao, sad, sid, gantry, colimador, x_res)

wl = WinstonLutz(path_to_dcm_file, use_filenames=True)
print(wl.results())
wl.plot_summary()

