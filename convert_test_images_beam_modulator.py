from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np
import glob
import os


list_mlc_model = ['MLCi2', 'Agility', 'Beam Modulator']
translacao = [0.0, 0.0]
sad = 1000.0
sid = 1600.0
gantry = 0.0
colimador = 0.0
x_res = 0.406
path_to_files = './images/BeamModulator/'
list_img_files = glob.glob(path_to_files + '*.tif')
tolerance = 0.5
action_tolerance = 0.3


for img in list_img_files:
    caminho,nome = os.path.split(os.path.splitext(img)[0])
    try:
        os.mkdir(caminho + '/PF_dicom/')
        os.mkdir(caminho + '/PF_pdf/')
        os.mkdir(caminho + '/PF_plot_image/')
        os.mkdir(caminho + '/PF_leaf_data/')
    except:
        print('Diretorios ja existem!')
        
    tiff_file = caminho + '/' + nome + '.tif'
    dcm_file = caminho + '/PF_dicom/' + nome + '.dcm'
    pdf_file = caminho + '/PF_pdf/' + nome + '.pdf'
    plot_img_file = caminho + '/PF_plot_image/' + nome + '.jpeg'
    ConvertToDicom.convert(nome, nome, tiff_file, dcm_file, translacao, sad, sid, gantry, colimador, x_res)
    if nome[0]=='E':
        nota_erros = 'Com erros propositais nos pares: 29, 07, 35, 23, 34, 03, 06, 11, 16'
    else:
        nota_erros = 'Sem erros propositais'
    meta_data = {'Autor': 'William A. P. dos Santos',
             'Função': 'Físico',
             'Unidade': 'ICESP',
             'Acelerador Linear': 'AL06',
             'Modelo MLC': list_mlc_model[2]}
    notes = ['Análise da variação de MU e largura da faixa',
             'Campo 16 cm X 20 cm',
             nota_erros,
             'Tolerância: ' + str(tolerance) + ' mm',
             'Limite de ação: ' + str(action_tolerance) + ' mm',
             'Arquivo de imagem: ' + nome + '.tif']
    pf = PicketFence(dcm_file)
    pf.analyze(mlc_model=list_mlc_model[2], tolerance=tolerance, action_tolerance=action_tolerance, orientation='u')
    pf.publish_pdf(filename=pdf_file, notes=notes, open_file=False, metadata=meta_data, customized=True)
    pf.save_analyzed_image(filename=plot_img_file, guard_rails=True, mlc_peaks=True, overlay=True, leaf_error_subplot=True)
    pickets = pf.get_test_pickets()
    #print(pf.results())
    text_file_erro = open(path_to_files + '/PF_leaf_data/Lista de erros.txt', "a")
    try:
        text_file = open(path_to_files + '/PF_leaf_data/Abs_values_' + nome + '.txt', "w")
        text_file2 = open(path_to_files + '/PF_leaf_data/' + nome + '.txt', "w")
        offsets = 'dist2cax'
        for pk in pickets:
            offsets +=  '\t' + f'{pk.dist2cax:2.3f}'
        errors_abs = np.zeros([pickets[0].error_array.shape[0],len(pickets)+1])
        errors = np.zeros([pickets[0].error_array_not_abs.shape[0],len(pickets)+1])
        for lin in range(0,errors.shape[0]):
            text_lin = ''
            text_lin_abs = ''
            for col in range(0,errors.shape[1]):
                if col==0:
                    if (lin==0):
                        text_header = 'Leaf'
                    errors_abs[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                    errors[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                    text_lin_abs = text_lin_abs + f'{errors_abs[lin,col]:2.0f}'
                    text_lin = text_lin + f'{errors[lin,col]:2.0f}'
                else:
                    if (lin==0):
                        text_header = text_header + f'\tPicket_{col}'
                    errors_abs[lin,col] = pickets[col-1].error_array[lin]
                    errors[lin,col] = pickets[col-1].error_array_not_abs[lin]
                    text_lin_abs = text_lin_abs + '\t' + f'{errors_abs[lin,col]:2.3f}'
                    text_lin = text_lin + '\t' + f'{errors[lin,col]:2.3f}'
            if (lin==0):
                text_file.write(text_header + '\n')
                text_file2.write(text_header + '\n')
            text_file.write(text_lin_abs + '\n')
            text_file2.write(text_lin + '\n')
        text_file.write(offsets + '\n')
        text_file2.write(offsets + '\n')
        text_file.close()
        text_file2.close()
    except:
        text_file_erro.write(nome + '.tif\n')
        text_file.close()
        text_file2.close()
        os.remove(path_to_files + '/PF_leaf_data/Abs_values_' + nome + '.txt')
        os.remove(path_to_files + '/PF_leaf_data/' + nome + '.txt')
    text_file_erro.close()
