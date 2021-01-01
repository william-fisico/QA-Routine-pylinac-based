import pandas as pd
#https://plotly.com/
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

df = pd.read_csv('./Historico_WL.dat', delimiter='\t')
df['Data'] = df['Data'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))

lista_imagens = ['Iso Gantry', 'Iso Colimador', 'Iso Gantry e Colimador', 'Iso Mesa',
                   'G0C0T0', 'G90C0T0', 'G180C0T0', 'G0C270T0', 'G270C0T0', 'G0C180T0', 'G0C90T0', 'G0C0T270', 'G0C0T90']
colors = {'Iso Gantry':'#1f77b4',
          'Iso Colimador':'#ff7f0e',
          'Iso Gantry e Colimador':'#2ca02c',
          'Iso Mesa':'#d62728',
          'G0C0T0':'#9467bd',
          'G90C0T0':'#8c564b',
          'G180C0T0':'#e377c2',
          'G0C270T0':'#7f7f7f',
          'G270C0T0':'#bcbd22',
          'G0C180T0':'#d62728',
          'G0C90T0':'#17becf',
          'G0C0T270':'#1a55FF',
          'G0C0T90':'#1a32cA'}
markers = {'Iso Gantry':'o',
          'Iso Colimador':'8',
          'Iso Gantry e Colimador':'p',
          'Iso Mesa':'1',
          'G0C0T0':'P',
          'G90C0T0':'3',
          'G180C0T0':'^',
          'G0C270T0':'>',
          'G270C0T0':'<',
          'G0C180T0':'P',
          'G0C90T0':'2',
          'G0C0T270':'*',
          'G0C0T90':'X'}

for imagem in lista_imagens:
    fig, ax = plt.subplots(1)
    ax.scatter(df['Data'],df[imagem], marker=markers[imagem], color=colors[imagem], label=imagem)
    x = mdates.date2num(df['Data'])
    residual_list = []
    fit_dict = {}
    for i in range(1,5):
        temp_fit = np.polyfit(x,df[imagem], i, full=True)
        try:
            residual_list.append(temp_fit[1][0])
            fit_dict[temp_fit[1][0]] = temp_fit
        except:
            print('')
    z = fit_dict[min(residual_list)][0]

    p = np.poly1d(z)
    x_dates_num = np.linspace(x.min()-1, x.max()+1, 100)
    x_dates = mdates.num2date(x_dates_num)
    plt.ylim(df[imagem].min() - 0.1*abs(df[imagem].min()),df[imagem].max() + 0.1*abs(df[imagem].max()))
    plt.xlim(x_dates[0],x_dates[-1])
    ax.plot(x_dates,p(x_dates_num),"r-",label='Tendencia')
    ax.grid(color='k', linestyle=':', which='major', linewidth=0.2)
    ax.legend(loc='best')
    ax.set_xlabel('Dia')
    ax.set_ylabel('Maior desvio (mm)')
    plt.title('Histórico do teste de Winston-Lutz - ' + imagem)
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.savefig('Historico/Historico_WL_' + imagem +'.jpeg', dpi=200)
    pdf = PdfPages('Historico/Historico_WL_' + imagem +'.pdf')
    pdf.savefig()
    pdf.close()
    #plt.show()
    plt.clf()
    

''' 
	ax.plot_date(list_date, list_dose, marker='.', color='b', ls=':', lw=0.2) #https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.axes.Axes.plot.html
    locator = mdates.AutoDateLocator() #(minticks=12, maxticks=24)
    ax.xaxis.set_major_locator(locator)
    formatter = DateFormatter('%d/%m/%y')
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=45, labelsize=7)
    ax.grid(color='k', linestyle=':', which='major', linewidth=0.2)
    #plt.show()
    plt.tight_layout()
    plt.savefig(path_to_files + 'Historico de ' + opt +'.jpeg', dpi=500)
    pdf = PdfPages(path_to_files + 'Historico de ' + opt +'.pdf')
    pdf.savefig()
    pdf.close()
    plt.clf()
'''