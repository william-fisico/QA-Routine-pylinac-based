from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np

path_to_test = './images/'
list_mlc_model = ['MLCi2', 'Agility']
translacao = [0.0, 0.0]
sad = 1000.0
sid = 1600.0
gantry = 0.0
colimador = 0.0
x_res = 0.406


for mlc_model in list_mlc_model:
    for mu in range(2,6):
        for picket_width in range(5,7):
            test_name = 'Picket_' + str(picket_width) + 'mm_' + str(mu) + 'MU'
            test_id = 'Picket_' + str(picket_width) + 'mm_' + str(mu) + 'MU'
            tiff_file = path_to_test + '/' + mlc_model + '/' + 'Picket-' + str(picket_width) + 'mm/Picket_' + str(picket_width) + 'mm_' + str(mu) + 'MU.tif'
            dcm_file = path_to_test + '/' + mlc_model + '/Dicom/Picket_' + str(picket_width) + 'mm_' + str(mu) + 'MU.dcm'
            pdf_file = path_to_test + '/' + mlc_model + '/PDF/Picket_' + str(picket_width) + 'mm_' + str(mu) + 'MU.pdf'
            data_file = path_to_test + '/' + mlc_model + '/Leaf_data/Picket_' + str(picket_width) + 'mm_' + str(mu) + 'MU.txt'
            if mlc_model == 'Agility':
                linac = 'Synergy Full'
            else:
                linac = 'Synergy Platform'
            meta_data = {'Autor': 'William A. P. dos Santos',
             'Função': 'Físico',
             'Unidade': 'Hospital',
             'Acelerador Linear': linac,
             'Modelo MLC': mlc_model}
            notes = ['Testando análise variação de MU e largura da faixa',
             'Campo 20 cm X 20 cm',
             'Largura da faixa = ' + str(picket_width) + 'mm',
             str(mu) + 'MU']

            ConvertToDicom.convert(test_name, test_id, tiff_file, dcm_file, translacao, sad, sid, gantry, colimador, x_res)
            pf = PicketFence(dcm_file)
            pf.analyze(mlc_model=mlc_model, tolerance=0.5, action_tolerance=0.3, orientation='u')
            pf.publish_pdf(filename=pdf_file, notes=notes, open_file=False, metadata=meta_data, customized=True)
            pickets = pf.get_test_pickets()
            errors = np.zeros([pickets[0].error_array.shape[0],len(pickets)+1])
            text_file = open(data_file, "w")
            for lin in range(0,errors.shape[0]):
                text_lin = ''
                for col in range(0,errors.shape[1]):
                    if col==0:
                        if lin==0:
                            text_header = 'Leaf'
                        errors[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                        text_lin = text_lin + f'{errors[lin,col]:2.0f}'
                    else:
                        if lin==0:
                            text_header = text_header + f'\tPicket {col}'
                        errors[lin,col] = pickets[col-1].error_array[lin]
                        text_lin = text_lin + '\t' + f'{errors[lin,col]:2.3f}'
                if lin==0:
                    text_file.write(text_header + '\n')
                text_file.write(text_lin + '\n')
            text_file.close()
            salvou = True
        
