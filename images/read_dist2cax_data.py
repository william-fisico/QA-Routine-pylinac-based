from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import glob

def criar_plot(arquivos, titulo, nome_pdf):

    path_to_files = './Images_31JUL2020/PF_leaf_data/'

    list_files = glob.glob(path_to_files + arquivos)
    #n_lines_plot = int((len(list_files) + 1)/2)
    fig, ax = plt.subplots(1)
    ax.set(xlabel='Distância para o CAX (mm)', ylabel='MU')
    fig.suptitle(titulo)
    cont_lin = 0
    cont_col = 0
    cont_color = -1
    color = ['b', 'g', 'r', 'c', 'm']

    for data_file in list_files:
        print(data_file)
        cont_color += 1
        infile = open(data_file, 'r')
        infile.readline()
        dist2cax = []
        text_values = [line.split()[1:len(line)-1] for line in infile]
        for lin in text_values:
            if (lin==text_values[-1]) or (lin==text_values[-2]):
                lin_value = []
                for col in lin:
                    lin_value.append(float(col))
                dist2cax.append(lin_value)
        mean_dist = []
        mu_value = []
        for x in range(0,len(dist2cax[0])):
            mean_dist.append((dist2cax[0][x] + dist2cax[1][x])/2)
            mu_value.append(float(data_file[-7]))
        dist2cax.append(mean_dist)
        dist2cax.append(mu_value)
        fmt=['o', 'x', 'd']
        cont_fmt = 0
        for data in dist2cax[0:-1]:
            media = 0
            maximo = 0
            for pos in range(0,len(data)-1):
                temp = data[pos] - data[pos+1]
                if pos==0:
                    maximo = temp
                    minimo = temp
                else:
                    if temp>maximo:
                        maximo = temp
                    if temp<minimo:
                        minimo = temp
                media += temp
            media = media/(len(data)-1)
            ax.plot(data, dist2cax[-1], marker=fmt[cont_fmt], color=color[cont_color], ls='')
            cont_fmt += 1
        ax.text(data[-3], 0.5+dist2cax[-1][0], f'Distância media = {media:2.2f} mm', color=color[cont_color])
        ax.text(1.2*data[-5], 0.2+dist2cax[-1][0], f'Distância máxima = {maximo:2.2f} mm', color=color[cont_color])
        ax.text(1.2*data[-1], 0.2+dist2cax[-1][0], f'Distância mínima = {minimo:2.2f} mm', color=color[cont_color])
    ax.grid(color='k', linestyle=':', which='major', linewidth=0.2)
    yticks = np.arange(0, 7, 1)
    xticks = np.arange(-100, 120, 20)
    ax.set_yticks(yticks)
    ax.set_xticks(xticks)
    pdf = PdfPages(path_to_files + nome_pdf)
    pdf.savefig()

    pdf.close()
    plt.clf()



lista_strip = ['5mm', '6mm']
for strip in lista_strip:
    arquivos = strip + '*.txt'
    titulo = 'Comparação MU com strip de ' + strip + ' - Distância para o CAX'
    nome_pdf = 'Comparacao_MU_strip_' + strip + '_dist2cax.pdf'
    criar_plot(arquivos, titulo, nome_pdf)
    #arquivos = 'Abs_values_' + strip + '*.txt'
    #titulo = titulo + ' - Valores absolutos'
    #nome_pdf = 'Comparacao_MU_strip_' + strip + '_Abs_values.pdf'
    #criar_histogramas(arquivos, titulo, nome_pdf)