from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np
'''
			
a = np.array([[1, 2], [3, 4], [5,6]])
print(np.mean(a,0))

'''

desloc = [0,0] #deslocamento do painel
ConvertToDicom.picketfence('G0C0Y2.tif','G0C0Y2_teste.dcm',desloc)#[20*(1600/1000),800])
ConvertToDicom.save_dicom('G0C0Y2_teste.dcm')
'''
ds = pydicom.filereader.read_file('G0C0Y2_teste.dcm')
print(ds[0x3002,0x000D])

plt.imshow(ds.pixel_array)
plt.show()
'''
pf_img = ['G0C0Y2_teste.dcm','EPID-PF-LR.dcm']
#pf_img = r"EPID-PF-LR.dcm"
x = ['MLCi2'] # ['Millennium MLC', 'Millennium HDMLC', 'Agility', 'MLCi2', 'Beam Modulator', 'MLC Primus']

for mlc in x:
	pf = PicketFence(pf_img[0])
	#print(mlc + " - Entrada")
	pf.analyze(mlc_model=mlc, tolerance=0.28, action_tolerance=0.279, orientation='u')
	print(pf.results())
	#pf.plot_analyzed_image(leaf_error_subplot = True)
