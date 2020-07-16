#######################################################
# William A. P. dos Santos                            #
# william.wapsantos@gmail.com                         #
# Interface para análise do picket fence              #
# 14 de julho de 2020                                 #
#######################################################

from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog,messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pydicom
import numpy as np
from PIL.TiffTags import TAGS

def teste():
    return

def atualizar_parametros(lista_entry):
    global gantry, colimador, sad, sid, x_res, translacao

    try:
        gantry = float(lista_entry[0][0].get())
        print(gantry)
    except:
        messagebox.showerror("Erro", "Valores inválidos")

def importar_img(eh_dicom): #Importa imagem a ser analisada
    global gantry, colimador, sad, sid, x_res, translacao

    importou = False
    if eh_dicom:
        tipos = (("Imagens DICOM","*.dcm"),("Todos os arquivos","*.*"))
        nome_arquivo = "G0C0Y2_teste.dcm"
    else :
        tipos = (("Imagens TIFF","*.tif"),("Todos os arquivos","*.*"))
        nome_arquivo = "G0C0Y1.tif"
    #nome_arquivo = filedialog.askopenfilename(initialdir='./', 
    #                title="Selecione o arquivo", filetypes=tipos)
    if nome_arquivo != "":
        if eh_dicom:
            try: #Abrir arquivo dicom
                ds = pydicom.filereader.read_file(nome_arquivo)
                image_array = ds.pixel_array
                try:
                    gantry = ds[0x300A,0x011E].value
                except:
                    gantry = 0.0
                try:
                    colimador = ds[0x300A,0x0120].value
                except:
                    colimador = 0.0
                try:
                    translacao = ds[0x3002,0x000D].value
                except:
                    translacao = [0.0,0.0]
                try:
                    sad = ds[0x3002,0x0022].value
                    sid = ds[0x3002,0x0026].value
                    x_res=ds[0x3002,0x0011].value[0]
                    dpmm = (1/x_res)*sid/sad #pontos por mm no isocentro
                    translacao = [translacao[0]/dpmm,translacao[1]/dpmm] # deslocamento em mm no painel
                except:
                    messagebox.showwarning("Aviso", "Imagem não possui informações importantes para o teste")
                importou = True
            except :
                messagebox.showwarning("Aviso", "Não foi possível abrir o arquivo selecionado")
        else:
            try:#Abrir arquivo TIFF
                tiff_file = Image.open(nome_arquivo)
                image_array = np.array(tiff_file)
                gantry = 0.0
                colimador = 0.0
                sad = 1000.0
                sid = 1600.0
                x_res = 0.406
                translacao = [0.0,0.0]
                importou = True
            except:
                messagebox.showwarning("Aviso", "Não foi possível abrir o arquivo selecionado")
            
        if importou: #cria a janela de importação com informações pertinentes
            janela_importar = Toplevel()
            janela_importar.title('importar imagem')
            janela_importar.iconbitmap('Imagens/dirac_eqn.ico')
            
            arquivo_label = Label(janela_importar, text="Imagem: "+nome_arquivo, justify=LEFT)
            gantry_label = Label(janela_importar,text="Gantry:", justify=LEFT)
            colimador_label = Label(janela_importar,text="Colimador:", justify=LEFT)
            sad_label = Label(janela_importar,text="SAD (mm):", justify=LEFT)
            sid_label = Label(janela_importar,text="SID (mm):", justify=LEFT)
            x_res_label = Label(janela_importar,text="Espaçamento entre pixels (mm): \n(Para Elekta Synergy usar 0.406 mm)", justify=CENTER)
            translacao_x_label = Label(janela_importar,text="translacao do painel em x (mm):", justify=LEFT)
            translacao_y_label = Label(janela_importar,text="translacao do painel em y (mm):", justify=LEFT)

            gantry_entry = Entry(janela_importar,width=8, borderwidth=5)
            colimador_entry = Entry(janela_importar,width=8, borderwidth=5)
            sad_entry = Entry(janela_importar,width=8, borderwidth=5)
            sid_entry = Entry(janela_importar,width=8, borderwidth=5)
            x_res_entry = Entry(janela_importar,width=8, borderwidth=5)
            translacao_x_entry = Entry(janela_importar,width=8, borderwidth=5)
            translacao_y_entry = Entry(janela_importar,width=8, borderwidth=5)

            lista_entry = [[gantry_entry, gantry],
                            [colimador_entry, colimador],
                            [sad_entry, sad],
                            [sid_entry, sid],
                            [x_res_entry, x_res],
                            [translacao_x_entry, translacao[0]],
                            [translacao_y_entry, translacao[1]]]

            lin = 0
            for entry in lista_entry:
                entry[0].grid(row=lin, column=5)
                entry[0].insert(0, entry[1])
                lin += 1

            lin = 0
            lista_label = [gantry_label, colimador_label, sad_label, sid_label, x_res_label, translacao_x_label, translacao_y_label]
            for label in lista_label:
                label.grid(row=lin,column=4)
                lin += 1

            fig = plt.Figure()
            fig.add_subplot(111).imshow(image_array)
            pf_img = FigureCanvasTkAgg(fig, janela_importar)
            pf_img.draw()
            pf_img.get_tk_widget().grid(row=1,column=0,rowspan=5, columnspan=3)
            



            arquivo_label.grid(row=0, column=0, columnspan=3)
            if eh_dicom:
                status_atualizar = DISABLED
            else:
                status_atualizar = NORMAL
            Button(janela_importar, text='Atualizar parâmetros', command=lambda: atualizar_parametros(lista_entry), state=status_atualizar).grid(row=7, column=0)
            Button(janela_importar, text='Importar', command=teste).grid(row=7, column=1)
            Button(janela_importar, text='Cancelar', command=janela_importar.destroy).grid(row=7, column=2)

            ##### tentar usar canvas para mostrar imagem em algum label
            #https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html

    else :
        messagebox.showwarning("Aviso", "Arquivo não selecionado")

    

####### Inicialização da Janel Principal #######
root = Tk()
root.title('Análise Picket Fence')
root.iconbitmap('Imagens/dirac_eqn.ico')
root.geometry("1400x720")
################################################

########### Criação da Barra de Menu ###########
menubar = Menu(root)

menu_arquivo = Menu(menubar, tearoff=0)
menu_arquivo.add_command(label="Importar imagem TIFF", command=lambda: importar_img(False))
menu_arquivo.add_command(label="Importar imagem DICOM", command=lambda: importar_img(True))
menu_arquivo.add_command(label="Excluir imagem selecionada", command=teste)
menu_arquivo.add_command(label="Excluir todas as imagens", command=teste)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Salvar resultados", command=root.quit)
menu_arquivo.add_command(label="Imprimir relatório", command=root.quit)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=root.quit)
menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

menu_opcoes = Menu(menubar, tearoff=0)
menu_opcoes.add_command(label="Editar informações da imagem", command=teste)
menu_opcoes.add_command(label="Critérios de análise", command=teste)
menu_opcoes.add_command(label="Opções de exibição dos resultados", command=teste)
menubar.add_cascade(label="Opções", menu=menu_opcoes)

menu_ajuda = Menu(menubar, tearoff=0)
menu_ajuda.add_command(label="Ajuda", command=teste)
menu_ajuda.add_separator()
menu_ajuda.add_command(label="Sobre", command=teste)
menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

root.config(menu=menubar)
################################################












root.mainloop()





