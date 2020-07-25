import matplotlib.pyplot as plt
import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import generate_uid
import numpy as np
from PIL import Image
from PIL.TiffTags import TAGS
import ConvertToDicom
from pylinac_dev import PicketFence

lista_imagens = ['G0C0Y1','G0C0Y1']

gantry = [0.0, 180.0]
colimador = [0.0, 180.0]
sad = [1000.0, 900.0]
sid = [1600.0, 1200.0]
translacao = [[0.0,0.0],[15.0, 20.0]]
x_res = 0.406

for cont in range(0,2):
    ConvertToDicom.convert(lista_imagens[cont], lista_imagens[cont], lista_imagens[cont]+'.tif',lista_imagens[cont]+'.dcm',translacao[cont], sad[cont], sid[cont], gantry[cont], colimador[cont], x_res)
    ds = pydicom.filereader.read_file(lista_imagens[cont]+'.dcm')
    print(ds)
    print('-----------------------------')
    pf = PicketFence(lista_imagens[cont]+'.dcm')
    pf.analyze(mlc_model='MLCi2', tolerance=0.285, action_tolerance=0.284, orientation='u')
    print(pf.results())

ds = pydicom.filereader.read_file('G0C0Y1_pfDicom.dcm')
print(ds)