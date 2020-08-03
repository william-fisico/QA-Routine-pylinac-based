from pylinac import PicketFence #importa modulo pylinac


img_dcm = './Arquivos_de_teste/dcm_Elekta.dcm' # local + nome do arquivo a ser analisado

pf = PicketFence(img_dcm) # inicializa o modulo
pf.analyze(tolerance=0.2, action_tolerance=0.1, orientation='u')
pf.plot_analyzed_image()
print(pf.results())
pf.publish_pdf(filename='./Arquivos_de_teste/teste_elekta.pdf')

