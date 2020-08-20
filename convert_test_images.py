from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np
import glob
import os

def converte_imagens(opt,eh_erro):
    list_mlc_model = ['MLCi2', 'Agility', 'Beam Modulator']
    translacao = [0.0, 0.0]
    sad = 1000.0
    sid = 1600.0
    gantry = 0.0
    colimador = 0.0
    x_res = 0.406
    path_to_files = './images/MLCi2/Images_12AGO2020/'
    list_img_files = glob.glob(path_to_files + opt)
    tolerance = 0.5
    action_tolerance = 0.3
    list_pickets = {}
    list_load_error = []


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
        if int(nome[4:6])==0:
            translacao = [0.0, 80.0]
        else:
            translacao = [0.0, -80.0]
        ConvertToDicom.convert(nome, nome, tiff_file, dcm_file, translacao, sad, sid, gantry, colimador, x_res)
        if nome[-5]=='E':
            nota_erros = 'Com erros propositais nos pares: 21, 20, 27, 14, 34, 18, 36, 04, 28'
        else:
            nota_erros = 'Sem erros propositais'
        meta_data = {'Autor': 'William A. P. dos Santos',
                 'Função': 'Físico',
                 'Acelerador Linear': 'Synergy Platform',
                 'Modelo MLC': list_mlc_model[0]}
        notes = ['Análise da variação de MU e largura da faixa',
                 'Campo 20 cm X 20 cm',
                 nota_erros,
                 'Tolerância: ' + str(tolerance) + ' mm',
                 'Limite de ação: ' + str(action_tolerance) + ' mm',
                 'Arquivo de imagem: ' + nome + '.tif']
        try:
            pf = PicketFence(dcm_file)
            pf.analyze(mlc_model=list_mlc_model[0], tolerance=tolerance, action_tolerance=action_tolerance, orientation='u')
            pf.publish_pdf(filename=pdf_file, notes=notes, open_file=False, metadata=meta_data, customized=True)
            pf.save_analyzed_image(filename=plot_img_file, guard_rails=True, mlc_peaks=True, overlay=True, leaf_error_subplot=True)
            list_pickets[nome] = pf.get_test_pickets()
            
        except:
        	list_load_error.append('Não foi possivel analisar o arquivo ' + dcm_file)

    print(list_load_error)

    strip_width_list = ['5mm', '6mm']
    list_field = ['20Y2x00Y1', '00Y2x20Y1']
    if eh_erro:
        img_mu_list = ['1MU_Erros', '2MU_Erros', '3MU_Erros', '4MU_Erros', '5MU_Erros']
    else:
        img_mu_list = ['1MU', '2MU', '3MU', '4MU', '5MU']


    for strip_width in strip_width_list:
        for img_mu in img_mu_list:
            nome_leaf_data = strip_width + '-20Y1x20Y2-' + img_mu + '.txt'
            try:
                text_file = open(path_to_files + '/PF_leaf_data/Abs_values_' + nome_leaf_data, "w")
                text_file2 = open(path_to_files + '/PF_leaf_data/' + nome_leaf_data, "w")
                offsets = {}
                for field in list_field:
                    nome_pickets = strip_width + '_' + field + '_' + img_mu
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
                                if (lin==0) & (field=='20Y2x00Y1'):
                                    text_header = 'Leaf'
                                errors_abs[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                                errors[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                                text_lin_abs = text_lin_abs + f'{errors_abs[lin,col]:2.0f}'
                                text_lin = text_lin + f'{errors[lin,col]:2.0f}'
                            else:
                                if (lin==0) & (field=='20Y2x00Y1'):
                                    text_header = text_header + f'\tPicket_{col}'
                                errors_abs[lin,col] = pickets[col-1].error_array[lin]
                                errors[lin,col] = pickets[col-1].error_array_not_abs[lin]
                                text_lin_abs = text_lin_abs + '\t' + f'{errors_abs[lin,col]:2.3f}'
                                text_lin = text_lin + '\t' + f'{errors[lin,col]:2.3f}'
                        if (lin==0) & (field=='20Y2x00Y1'):
                            text_file.write(text_header + '\n')
                            text_file2.write(text_header + '\n')
                        text_file.write(text_lin_abs + '\n')
                        text_file2.write(text_lin + '\n')
                text_file.write(offsets['20Y2x00Y1'] + '\n')
                text_file.write(offsets['00Y2x20Y1'] + '\n')
                text_file2.write(offsets['20Y2x00Y1'] + '\n')
                text_file2.write(offsets['00Y2x20Y1'] + '\n')
                text_file.close()
                text_file2.close()
            except:
                list_load_error.append('Não foi possivel analisar o arquivo ' + nome_leaf_data)

    text_file_erro = open(path_to_files + '/PF_leaf_data/Lista de erros.txt', "w")
    for load_error in list_load_error:
        text_file_erro.write(load_error + '\n')
    text_file_erro.close()
    return 'Finalizou'


def analisa_erros(arquivos, titulo, nome_comp):
    erro_esperado = {'1': ['21',-1.0], '2': ['20',1.0], '3': ['27',-1.5], '4': ['14',-1.0], '5': ['34',-0.5],
                     '6': ['18',1.5], '7': ['36',-1.0], '8': ['4',0.5], '9': ['28',0.5]} # erro_esperado = {'# picket': [# para mlc, valor esperado (mm)]}
    path_to_files = './images/MLCi2/Images_12AGO2020/PF_leaf_data/'
    list_files = glob.glob(path_to_files + arquivos)
    print(path_to_files + arquivos)
    for data_file in list_files:
        #cont_color += 1
        caminho,nome = os.path.split(os.path.splitext(data_file)[0])
        if (nome[0] == '5') or (nome[0] == '6'):
            print(nome[-9:-6])
            infile = open(data_file, 'r')
            infile.readline()
            lista_linha = [line.split() for line in infile]
            text_file_errors = open(path_to_files + nome_comp + nome[0:3] + '_' + nome[-9:-6] + '.txt', "w")
            header_errors = 'Picket\tPar MLC\tErro esperado (mm)\tErro medido (mm)\tDif. abs. (mm)\tDif. rel.'
            text_file_errors.write(header_errors + '\n')
            for picket in erro_esperado:
                idx_pk = int(picket)
                idx_mlc = int(erro_esperado[picket][0])
                #output_line = [#par mlc, erro esperado, erro medido, dif abs, dif rel]
                output_line = [erro_esperado[picket][0], f'{float(erro_esperado[picket][1]):2.3f}',
                               f'{float(lista_linha[idx_mlc-1][idx_pk]):2.3f}', f'{float(lista_linha[idx_mlc-1][idx_pk])-float(erro_esperado[picket][1]):2.3f}',
                               f'{(float(lista_linha[idx_mlc-1][idx_pk])-float(erro_esperado[picket][1]))/float(erro_esperado[picket][1]):2.3f}']
                saida = picket
                for output in output_line:
                    saida += '\t' + output
                text_file_errors.write(saida + '\n')



list_opt = ['*MU.tif', '*Erros.tif']
list_bool = {'*MU.tif':False, '*Erros.tif':True}
opt = list_opt[1]
#temp = converte_imagens(opt, list_bool[opt])
if list_bool[opt]:
    titulo = 'Análise dos erros com strip de '
    nome_comparacao = 'Analise_erros_MU_strip_'
    analisa_erros('*Erros.txt', titulo, nome_comparacao)


