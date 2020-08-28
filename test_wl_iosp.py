from pylinac_dev import WinstonLutz
import ConvertToDicom
import pydicom #https://pydicom.github.io/pydicom/stable/tutorials/
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import glob
import os

lista_resultado = ['Nome', 'Iso Gantry', 'Iso Colimador', 'Iso Gantry e Colimador', 'Iso Mesa',
                   'G0C0T0', 'G90C0T0', 'G180C0T0', 'G270C0T0', 'G0C90T0', 'G0C270T0', 'G0C0T90', 'G0C0T270']
root_col = './Teste_26AGO2020/Colimador'
root_gantry = './Teste_26AGO2020/Gantry'
root_mesa = './Teste_26AGO2020/Mesa'
root_list = [root_col, root_gantry, root_mesa]

ang_list = {'1': 181.0}
for i in range(2,26):
    ang = -165.0 + 15*(i-2)
    if ang<0:
        ang += 360
    ang_list[str(i)] = ang
mesa_ang_list = {}
for j in range (1,14):
    if j<8:
        ang = 0.0 + 15*(j-1)
    else:
        ang = 345.0 + 15*(8-j)
    mesa_ang_list[str(j)] = ang

path_to_jpg_file = './Teste_26AGO2020/imagem.jpg'
path_to_pdf_file = './Teste_26AGO2020/relatorio.pdf'
path_to_dcm_file = './Teste_26AGO2020/WL_dcm'
try:
    os.mkdir(path_to_dcm_file)
except:
    print('ok')
meta_data = {'Autor': 'William A. P. dos Santos',
                 'Função': 'Físico',
                 'Acelerador Linear': 'Synergy Full',
                 'Modelo MLC': 'Agility'}
notes = ['Análise de Winston-Lutz com pylinac',
         'Campo 2 cm X 2 cm',
         'Tolerância: 1 mm',
         'Limite de ação: 0.8 mm',
         'Local das imagens: ' + path_to_jpg_file]

for folder in root_list:
    list_img_files = glob.glob(folder + '/*.tif')
    path_to_folder,folder_name = os.path.split(os.path.splitext(folder)[0])
    translacao = [0.0, 0.0]
    sad = 1000.0
    sid = 1600.0
    gantry = 0.0
    colimador = 0.0
    mesa = 0.0
    for img in list_img_files:
        caminho,nome = os.path.split(os.path.splitext(img)[0])
        tiff_file = caminho + '/' + nome + '.tif'
        if folder==root_gantry:
            gantry = ang_list[nome]
            colimador = 0.0
            mesa = 0.0
            dcm_file = path_to_dcm_file + '/gantry_' + nome + '.dcm'
        elif folder==root_col:
            gantry = 0.0
            colimador = ang_list[nome]
            mesa = 0.0
            dcm_file = path_to_dcm_file + '/colimador_' + nome + '.dcm'
        elif folder==root_mesa:
            gantry = 0.0
            colimador = 0.0
            mesa = mesa_ang_list[nome]
            dcm_file = path_to_dcm_file + '/mesa_' + nome + '.dcm'
        else:
            gantry = 0.0
            colimador = 0.0
            mesa = 0.0
        ConvertToDicom.convert(nome, nome, tiff_file, dcm_file, translacao, sad, sid, gantry, colimador, mesa=mesa)

wl = WinstonLutz(path_to_dcm_file, use_filenames=False)
#print(wl.results())
#wl.plot_summary()
wl.save_summary(path_to_jpg_file)
wl.publish_pdf(filename=path_to_pdf_file, notes=notes, open_file=False, metadata=meta_data, customized=True)

