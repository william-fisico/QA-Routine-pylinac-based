from pylinac_dev import PicketFence

pf_img = ['G0C0Y2.dcm']
#pf_img = r"EPID-PF-LR.dcm"
x = ['Millennium MLC', 'Millennium HDMLC', 'Agility', 'MLCi2', 'Beam Modulator', 'MLC Primus']

for mlc in x:
	pf = PicketFence(pf_img[0])
	print(mlc + " - Entrada")
	pf.analyze(mlc_model=mlc, tolerance=0.292, action_tolerance=0.291)
	#pf.plot_analyzed_image(leaf_error_subplot = True)
	#print(pf.results())
