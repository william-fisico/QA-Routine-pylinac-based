from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np

#lista_img = [[Nome imagem],[desloc painel]]
lista_img = [["0Y2-10Y1", [0.0,80.0]], ["0Y2-20Y1", [0.0,80.0]], ["5Y2-20Y1", [0.0,80.0]],
			 ["10Y2-0Y1", [0.0,-80.0]], ["20Y2-0Y1", [0.0,-80.0]], ["20Y2-5Y1", [0.0,-80.0]],
			 ["10Y2-10Y1", [0.0,0.0]], ["10Y2-10Y1-ERRO2", [0.0,0.0]], ["10Y2-10Y1-ERRO3", [0.0,0.0]]]
# Painel deslocado na direção de Y2 (iso para inferior) ==> y<0
# Painel deslocado na direção de Y1 (iso para superior) ==> y>0


sad = 1000.0 # mm
sid = 1600.0 # mm
gantry = 0.0
colimador = 0.0
x_res = 0.406
num_pickets = 9

for img in lista_img:
	ConvertToDicom.convert('./Imagens/'+img[0]+'.tif','./Imagens/'+img[0]+'.dcm',img[1], sad, sid, gantry, colimador, x_res)
	pf = PicketFence('./Imagens/'+img[0]+'.dcm')
	pf.analyze(mlc_model='MLCi2', tolerance=1, action_tolerance=0.8, num_pickets=num_pickets, invert=False, orientation='u')
	notas = ['Testando análise com deslocamento do painel',
			 'Análise da Imagem: '+img[0],
			 'Deslocamento do painel em Y: ' + str(img[1][1]/10) + ' cm']

	dados = {'Autor': 'William A. P. dos Santos',
			 'Função': 'Físico',
			 'Unidade': 'Hospital',
			 'Acelerador Linear': 'Synergy Platform',
			 'Modelo MLC': 'MLCi2'}

	pf.publish_pdf('./Imagens/'+img[0]+'.pdf', notas, open_file=False, metadata=dados)