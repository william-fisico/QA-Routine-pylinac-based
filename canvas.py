from tkinter import *
from PIL import ImageTk,Image
import numpy as np
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = Tk()

nome_arquivo = "G0C0Y2_teste.dcm"
ds = pydicom.filereader.read_file(nome_arquivo)
data = ds.pixel_array
root.geometry(str(data.shape[0])+"x"+str(data.shape[1]))

fig = plt.Figure()
fig.add_subplot(111).imshow(data)
chart_type = FigureCanvasTkAgg(fig, root)
chart_type.draw()
chart_type.get_tk_widget().grid(row=1,column=1)


root.mainloop()