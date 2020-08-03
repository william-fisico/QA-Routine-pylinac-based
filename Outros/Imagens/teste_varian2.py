from pylinac_dev import PicketFence #importa modulo pylinac editado
import numpy as np


img_dcm = './Arquivos_de_teste/dcm_Varian.dcm' # local + nome do arquivo a ser analisado

pf = PicketFence(img_dcm) # inicializa o modulo
pf.analyze(tolerance=0.2, action_tolerance=0.1, orientation='l', mlc_model='Millennium MLC')
pf.plot_analyzed_image()
print(pf.results())
pf.publish_pdf(filename='./Arquivos_de_teste/teste_varian.pdf', customized=True)


pickets = pf.get_test_pickets()
errors = np.zeros([pickets[0].error_array.shape[0],len(pickets)+1])
text_file = open('./Arquivos_de_teste/teste_varian2.txt', "w")
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
        


