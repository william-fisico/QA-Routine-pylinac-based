from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import glob

def criar_histogramas(arquivos, titulo, nome_pdf):

    path_to_files = './BeamModulator/PF_leaf_data/'

    list_files = glob.glob(path_to_files + arquivos)
    n_lines_plot = int((len(list_files) + 1)/2)
    fig, ax = plt.subplots(n_lines_plot,2)
    fig.suptitle(titulo)
    leaf_error_list = []
    cont_lin = 0
    cont_col = 0

    for data_file in list_files:
        infile = open(data_file, 'r')
        infile.readline()
        leaf_error = []
        text_values = [line.split()[1:len(line)-1] for line in infile]
        for lin in text_values:
            if (lin!=text_values[-1]):
                for col in lin:
                    leaf_error.append(float(col))
        leaf_error_list.append(leaf_error)

        (mu, sigma) = norm.fit(leaf_error) # best fit of data
        print(mu,sigma)

        n, bins, patches = ax[cont_lin][cont_col].hist(x=leaf_error, bins='auto', color='#0504aa',
                                density=True,alpha=0.7, rwidth=0.85)
        # add a 'best fit' line
        norm_fit = norm.pdf(bins, mu, sigma)
        l = ax[cont_lin][cont_col].plot(bins, norm_fit, 'r--', linewidth=2)
        ax[cont_lin][cont_col].grid(axis='y', alpha=0.75)
        #ax[cont_lin][cont_col].xlabel('Value')
        #ax[cont_lin][cont_col].ylabel('Frequency')
        #ax[cont_lin][cont_col].title('My Very Own Histogram')
        ax[cont_lin][cont_col].text(1.05*min(bins), 0.85*max(n), data_file[-7:-4])
        ax[cont_lin][cont_col].text(1.05*min(bins), 0.65*max(n), f'\u03BC = {mu:2.2f}mm') #https://pythonforundergradengineers.com/unicode-characters-in-python.html
        ax[cont_lin][cont_col].text(1.05*min(bins), 0.45*max(n), f'\u03C3 = {sigma:2.2f}mm') #https://pythonforundergradengineers.com/unicode-characters-in-python.html

        #ax[cont_lin][cont_col].text(0.25, 5, data_file[-7:-4])
        maxfreq = n.max()
        # Set a clean upper y-axis limit.
        #ax[cont_lin][cont_col].ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
        #ax[cont_lin][cont_col].savefig(data_file + '.png')
        cont_col += 1
        if cont_col == 2:
            cont_col = 0
            cont_lin += 1
    ax[cont_lin][cont_col].axis('off')

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.15, hspace=0.25)
    #fig.tight_layout()
    pdf = PdfPages(path_to_files + nome_pdf)
    pdf.savefig()

    pdf.close()
    plt.clf()

def analisa_erros(arquivos, titulo, nome_comp):
    erro_esperado = {'1': ['29',-1.0], '2': ['7',-0.5], '3': ['35',0.5], '4': ['23',-1.5], '5': ['34',-0.5],
                     '6': ['3',1.0], '7': ['6',0.5], '8': ['11',-0.5], '9': ['16',1.0]} # erro_esperado = {'# picket': [# para mlc, valor esperado (mm)]}
    path_to_files = './BeamModulator/PF_leaf_data/'
    list_files = glob.glob(path_to_files + arquivos)
    for data_file in list_files:
        #cont_color += 1
        infile = open(data_file, 'r')
        infile.readline()
        lista_linha = [line.split() for line in infile]
        text_file_errors = open(path_to_files + nome_comp + '-' +data_file[-7:-4] + '.txt', "w")
        header_errors = 'Picket\tPar MLC\tErro esperado (mm)\tErro medido (mm)\tDif. abs. (mm)\tDif. rel.'
        text_file_errors.write(header_errors + '\n')
        for picket in erro_esperado:
            idx_pk = int(picket)
            idx_mlc = int(erro_esperado[picket][0])
            #output_line = [#par mlc, erro esperado, erro medido, dif abs, dif rel]
            output_line = [erro_esperado[picket][0], f'{float(erro_esperado[picket][1]):2.3f}',
                           f'{float(lista_linha[idx_mlc-1][idx_pk]):2.3f}', f'{float(lista_linha[idx_mlc-1][idx_pk])-float(erro_esperado[picket][1]):2.3f}',
                           f'{(float(lista_linha[idx_mlc-1][idx_pk])-float(erro_esperado[picket][1]))/float(erro_esperado[picket][1]):2.3f}']
            saida = picket
            for output in output_line:
                saida += '\t' + output
            text_file_errors.write(saida + '\n')


lista_strip = ['5mm', '6mm', '10mm','Erros-5mm', 'Erros-6mm', 'Erros-10mm']
for strip in lista_strip:
    arquivos = strip + '*.txt'
    titulo = 'Comparação MU com strip de' + strip
    nome_pdf = 'Comparacao_MU_strip_' + strip + '.pdf'
    criar_histogramas(arquivos, titulo, nome_pdf)
    if strip[0]=='E':
        titulo = 'Análise dos erros com strip de ' + strip[6:len(strip)]
        nome_comparacao = 'Analise_erros_MU_strip_' + strip
        analisa_erros(arquivos, titulo, nome_comparacao)
        