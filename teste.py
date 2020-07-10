from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
ConvertToDicom.picketfence('G0C0Y2.tif','G0C0Y2_teste.dcm',[0,80])#[20*(1600/1000),800])
ConvertToDicom.save_dicom('G0C0Y2_teste.dcm')

ds = pydicom.filereader.read_file('G0C0Y2_teste.dcm')
print(ds[0x3002,0x000D])
'''
plt.imshow(ds.pixel_array)
plt.show()
'''
pf_img = ['G0C0Y2_teste.dcm','EPID-PF-LR.dcm']
#pf_img = r"EPID-PF-LR.dcm"
x = ['MLCi2'] # ['Millennium MLC', 'Millennium HDMLC', 'Agility', 'MLCi2', 'Beam Modulator', 'MLC Primus']

for mlc in x:
	pf = PicketFence(pf_img[0])
	#print(mlc + " - Entrada")
	pf.analyze(mlc_model=mlc, tolerance=0.292, action_tolerance=0.291, orientation='u')
	pf.plot_analyzed_image(leaf_error_subplot = True)
	print(pf.results())
	
