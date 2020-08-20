from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import glob

def criar_histogramas(arquivos, titulo, nome_pdf):

    path_to_files = './MLCi2/Images_12AGO2020/PF_leaf_data/'

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
            if (lin!=text_values[-1]) and (lin!=text_values[-2]):
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

lista_strip = ['5mm', '6mm']
for strip in lista_strip:
    arquivos = strip + '*MU_Erros.txt'
    titulo = 'Comparação MU com strip de' + strip
    nome_pdf = 'Comparacao_MU_strip_' + strip + '_Erros.pdf'
    try:
        criar_histogramas(arquivos, titulo, nome_pdf)
    except:
        print('ok')
    #arquivos = 'Abs_values_' + strip + '*.txt'
    #titulo = titulo + ' - Valores absolutos'
    #nome_pdf = 'Comparacao_MU_strip_' + strip + '_Abs_values.pdf'
    #criar_histogramas(arquivos, titulo, nome_pdf)