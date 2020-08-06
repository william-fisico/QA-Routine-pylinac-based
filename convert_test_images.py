from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np
import glob
import os


list_mlc_model = ['MLCi2', 'Agility']
translacao = [0.0, 0.0]
sad = 1000.0
sid = 1600.0
gantry = 0.0
colimador = 0.0
x_res = 0.406
path_to_files = './images/Images_31JUL2020/'
list_img_files = glob.glob(path_to_files + '*.tif')
tolerance = 0.5
action_tolerance = 0.3
list_pickets = {}


for img in list_img_files:
    caminho,nome = os.path.split(os.path.splitext(img)[0])
    tiff_file = caminho + '/' + nome + '.tif'
    dcm_file = caminho + '/PF_dicom/' + nome + '.dcm'
    pdf_file = caminho + '/PF_pdf/' + nome + '.pdf'
    plot_img_file = caminho + '/PF_plot_image/' + nome + '.jpeg'
    if int(nome[4:6])==0:
        translacao = [0.0, -80.0]
    else:
        translacao = [0.0, 80.0]
    ConvertToDicom.convert(nome, nome, tiff_file, dcm_file, translacao, sad, sid, gantry, colimador, x_res)
    meta_data = {'Autor': 'William A. P. dos Santos',
             'Função': 'Físico',
             'Unidade': 'ICESP',
             'Acelerador Linear': 'AL02',
             'Modelo MLC': list_mlc_model[0]}
    notes = ['Análise da variação de MU e largura da faixa',
             'Campo 20 cm X 20 cm',
             'Sem erros propositais',
             'Tolerância: ' + str(tolerance) + ' mm',
             'Limite de ação: ' + str(action_tolerance) + ' mm',
             'Arquivo de imagem: ' + nome + '.tif']
    pf = PicketFence(dcm_file)
    pf.analyze(mlc_model=list_mlc_model[0], tolerance=tolerance, action_tolerance=action_tolerance, orientation='u')
    pf.publish_pdf(filename=pdf_file, notes=notes, open_file=False, metadata=meta_data, customized=True)
    pf.save_analyzed_image(filename=plot_img_file, guard_rails=True, mlc_peaks=True, overlay=True, leaf_error_subplot=True)
    list_pickets[nome] = pf.get_test_pickets()
    #print(pf.results())

strip_width_list = ['5mm', '6mm']
list_field = ['00Y1x20Y2', '20Y1x00Y2']
img_mu_list = ['1MU', '2MU', '3MU', '4MU', '5MU']

for strip_width in strip_width_list:
    for img_mu in img_mu_list:
        nome_leaf_data = strip_width + '-20Y1x20Y2-' + img_mu + '.txt'
        text_file = open(path_to_files + '/PF_leaf_data/Abs_values_' + nome_leaf_data, "w")
        text_file2 = open(path_to_files + '/PF_leaf_data/' + nome_leaf_data, "w")
        offsets = {}
        for field in list_field:
            nome_pickets = strip_width + '-' + field + '-' + img_mu
            pickets = list_pickets[nome_pickets]
            offsets[field] = field + '_dist2cax'
            for pk in pickets:
                offsets[field] = offsets[field] + '\t' + f'{pk.dist2cax:2.3f}'
            errors_abs = np.zeros([pickets[0].error_array.shape[0],len(pickets)+1])
            errors = np.zeros([pickets[0].error_array_not_abs.shape[0],len(pickets)+1])
            for lin in range(0,errors.shape[0]):
                text_lin_abs = ''
                text_lin = ''
                for col in range(0,errors.shape[1]):
                    if col==0:
                        if (lin==0) & (field=='00Y1x20Y2'):
                            text_header = 'Leaf'
                        errors_abs[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                        errors[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                        text_lin_abs = text_lin_abs + f'{errors_abs[lin,col]:2.0f}'
                        text_lin = text_lin + f'{errors[lin,col]:2.0f}'
                    else:
                        if (lin==0) & (field=='00Y1x20Y2'):
                            text_header = text_header + f'\tPicket_{col}'
                        errors_abs[lin,col] = pickets[col-1].error_array[lin]
                        errors[lin,col] = pickets[col-1].error_array_not_abs[lin]
                        text_lin_abs = text_lin_abs + '\t' + f'{errors_abs[lin,col]:2.3f}'
                        text_lin = text_lin + '\t' + f'{errors[lin,col]:2.3f}'
                if (lin==0) & (field=='00Y1x20Y2'):
                    text_file.write(text_header + '\n')
                    text_file2.write(text_header + '\n')
                text_file.write(text_lin_abs + '\n')
                text_file2.write(text_lin + '\n')
        text_file.write(offsets['00Y1x20Y2'] + '\n')
        text_file.write(offsets['20Y1x00Y2'] + '\n')
        text_file2.write(offsets['00Y1x20Y2'] + '\n')
        text_file2.write(offsets['20Y1x00Y2'] + '\n')
        text_file.close()
        text_file2.close()
            
