from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np

'''		
a = np.array([0,1,2,3,4,5,6,7,8,9,10])
print(np.flip(a))
'''
# Painel deslocado na direção de Y2 (iso para inferior) ==> y>0
desloc = [0.0,70.0] #deslocamento do painel em mm 
sad = 1000.0 # mm
sid = 1600.0 # mm
ConvertToDicom.picketfence('G0C0Y2.tif','G0C0Y2_teste.dcm',desloc, sad, sid)
ConvertToDicom.save_dicom('G0C0Y2_teste.dcm')
#ds = pydicom.filereader.read_file('EPID-PF-LR.dcm')
#print(ds)
'''
plt.imshow(ds.pixel_array)
plt.show()
'''
pf_img = ['G0C0Y2_teste','EPID-PF-LR']
#pf_img = r"EPID-PF-LR.dcm"
x = ['MLCi2'] # ['Millennium MLC', 'Millennium HDMLC', 'Agility', 'MLCi2', 'Beam Modulator', 'MLC Primus']

for mlc in x:
	pf = PicketFence(pf_img[0] + '.dcm')
	#print(mlc + " - Entrada")
	pf.analyze(mlc_model=mlc, tolerance=0.285, action_tolerance=0.284, orientation='u')
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
'''
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

