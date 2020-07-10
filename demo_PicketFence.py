###########################################
# William A. P. dos Santos                #
# william.wapsantos@gmail.com             #
# Testanto Pylinac                        #
# 02 de julho de 2020                     #
###########################################

from pylinac_dev import PicketFence

pf_img = ['G0C0Y2']
#pf_img = r"EPID-PF-LR.dcm"
for nome in pf_img:
	pf = PicketFence(nome + '.dcm')
	pf.analyze(tolerance=0.292, action_tolerance=0.291, hdmlc = False)
	pf.plot_analyzed_image(leaf_error_subplot = True)
	print(pf.results())
	pf.publish_pdf(filename = nome + '.pdf')

'''
#PicketFence.run_demo()
pf = PicketFence.from_demo_image()
pf.analyze(tolerance=0.05, action_tolerance=0.03)
# print results to the console
print(pf.results())
# view analyzed image
pf.plot_analyzed_image()
# save PDF report
#pf.publish_pdf(filename='Demo Picket Fence.pdf')


#pf = PicketFence.from_demo_image()
#print(type(pf))'''