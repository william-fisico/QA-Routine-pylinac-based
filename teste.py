from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np

'''		
a = np.array([0,1,2,3,4,5,6,7,8,9,10])
print(np.flip(a))

# Painel deslocado na direção de Y2 (iso para inferior) ==> y<0
# Painel deslocado na direção de Y1 (iso para superior) ==> y>0
desloc = [0.0,80.0] #deslocamento do painel em mm 
sad = 1000.0 # mm
sid = 1600.0 # mm
ConvertToDicom.convert('./Imagens/0Y2-20Y1.tif','./Imagens/0Y2-20Y1.dcm',desloc, sad, sid,0.0,0.0, 0.406)
#ConvertToDicom.save_dicom('/Imagens/MLCi2/TESTE/10Y2-10Y1/10Y2-10Y1-ERRO3.dcm')
#ds = pydicom.filereader.read_file('EPID-PF-LR.dcm')
#print(ds)

plt.imshow(ds.pixel_array)
plt.show()

pf_img = ['./Imagens/0Y2-20Y1','EPID-PF-LR']
'''
x = ['MLCi2'] # ['Millennium MLC', 'Millennium HDMLC', 'Agility', 'MLCi2', 'Beam Modulator', 'MLC Primus']

for mlc in x:
    pf = PicketFence('10Y2-10Y1_pfDicom' + '.dcm')
    pf.analyze(mlc_model=mlc, tolerance=0.285, action_tolerance=0.284, orientation='u')
    pickets = pf.get_test_pickets()
    erros = np.zeros([pickets[0].error_array.shape[0],len(pickets)+1])
    text_file = open("sample.txt", "w")
    for lin in range(0,erros.shape[0]):
        texto_lin = ''
        for col in range(0,erros.shape[1]):
            if col==0:
                if lin==0:
                    texto_header = 'Leaf'
                erros[lin,col] = pickets[col].leafs_idx_in_picket[lin]
                texto_lin = texto_lin + f'{erros[lin,col]:2.0f}'
            else:
                if lin==0:
                    texto_header = texto_header + f'\tPicket {col}'
                erros[lin,col] = pickets[col-1].error_array[lin]
                texto_lin = texto_lin + '\t' + f'{erros[lin,col]:2.3f}'
        if lin==0:
            text_file.write(texto_header + '\n')
        text_file.write(texto_lin + '\n')
    text_file.close()
    

'''
    cont = 1
    for picket in pickets:
        print('-------Picket-----------', cont)
        cont += 1
        for i in range(0,picket.error_array.shape[0]):
            print(picket.leafs_idx_in_picket[i], picket.error_array[i])

    print(pf.results())
    pf.plot_analyzed_image(guard_rails=False, mlc_peaks=True, overlay=True,
                            leaf_error_subplot=True, show=True)

    notas = ['Testando análise com deslocamento do painel',
			 'Campo 26 cm X 6 cm - Assimétrico em Y',
			 'Y1 = 6 cm e Y2 = 20 cm',
			 'Lâminas 1 e 26 não foram incluídas na análise']

    dados = {'Autor': 'William A. P. dos Santos',
			 'Função': 'Físico',
			 'Unidade': 'Hospital',
			 'Acelerador Linear': 'Synergy Platform',
			 'Modelo MLC': 'MLCi2'}

	#pf.publish_pdf(filename='/Teste.pdf', notes=notas, open_file=False, metadata=dados)

	#recebe todos os pickets, número das lâminas na imagem e imprime o erro de 
	#cada lâmina em cada picket
	pickets,leafs_idx_in_image = pf.get_test_pickets()
	cont = 1
	for picket in pickets:
		print('----------------- Picket ', cont, ' -----------------')
		cont += 1
		try:
			for i in range(0,picket.error_array.shape[0]):
				text = f'Erro de {picket.error_array[-i-1]:2.3f} mm na lamina {leafs_idx_in_image[-i-1]}'
				print(text)
		except:
			print('Erro')
'''
