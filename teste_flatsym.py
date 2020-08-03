from pylinac_dev import FlatSym
import ConvertToDicom


lista_img = ['PORTAL_6MV_5MU', 'PORTAL_6MV_2MU','PORTAL_10MV_2MU']

for img in lista_img:
    nome_teste = img
    id_teste = img
    filename = 'Teste_FlatSym/' + img + '.tif'
    nome_dcm = 'Teste_FlatSym/' + img + '.dcm'
    nome_pdf = 'Teste_FlatSym/' + img + '.pdf'
    translacao = [0.0,0.0]
    sad = 1000.0
    sid = 1600.0
    gantry = 0.0
    colimador = 0.0
    x_res = 0.406
    ConvertToDicom.convert(nome_teste, id_teste, filename, nome_dcm, translacao, sad, sid, gantry, colimador, x_res)

    my_flatsym = FlatSym(path=nome_dcm)
    my_flatsym.analyze(flatness_method='elekta', symmetry_method='elekta', vert_position=0.5, horiz_position=0.5, invert=True)
    #print(my_flatsym.results())
    #my_flatsym.plot_analyzed_image()
    meta_data = {'Autor': 'William A. P. dos Santos',
             'Função': 'Físico',
             'Unidade': 'Hospital',
             'Acelerador Linear': 'Synergy',
             'Modelo MLC': 'MLC',
             'Tamanho de campo': '20 cm X 20 cm'}
    #notes = ['Testando análise de simetria e planura', 'Imagem ' + img]
    my_flatsym.publish_pdf(filename=nome_pdf, metadata=meta_data, customized=True)
