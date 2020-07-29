from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np

pf = PicketFence('EPID-PF-LR' + '.dcm')
pf.analyze(mlc_model='Millennium HDMLC', tolerance=0.285, action_tolerance=0.284, orientation='l')
notas = ['Testando análise com deslocamento do painel',
             'Campo 26 cm X 6 cm - Assimétrico em Y',
             'Y1 = 6 cm e Y2 = 20 cm',
             'Lâminas 1 e 26 não foram incluídas na análise']

dados = {'Autor': 'William A. P. dos Santos',
             'Função': 'Físico',
             'Unidade': 'Hospital',
             'Acelerador Linear': 'Synergy Platform',
             'Modelo MLC': 'MLCi2'}

pf.publish_pdf(filename='Teste_custom.pdf', notes=notas, open_file=False, metadata=dados, customized=True)
