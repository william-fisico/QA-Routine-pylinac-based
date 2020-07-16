#######################################################
# William A. P. dos Santos                            #
# william.wapsantos@gmail.com                         #
# Convertendo TIFF para Dicom                         #
# 05 de julho de 2020                                 #
#                                                     #
# Este módulo foi desenvolvido para converter imagens #
# no formato Tiff para Dicom. O módulo foi pensado    #
# para tratar imagnes geradas pelo software Iview,    #
# utilizado para aquisição de imagem planar em        #
# aceleradores Elekta, e analisadas com auxílio da    #
# biblioteca Pylinac                                  #
#######################################################


# Referencia para criar arquivo Dicom: https://pydicom.github.io/pydicom/dev/auto_examples/input_output/plot_write_dicom.html#sphx-glr-auto-examples-input-output-plot-write-dicom-py

import os
import tempfile
import datetime
import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from PIL import Image
from PIL.TiffTags import TAGS
import numpy as np
import matplotlib.pyplot as plt

def convert(nome_tiff, nome_dicom, translacao, sad, sid, gantry, colimador, x_res):
	global ds
	# Nome do arquivo
	filename_little_endian = nome_dicom

	# Criando arquivos com informações minimas
	#print('Criando arquivo Dicom Image')
	file_meta = FileMetaDataset()
	file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.1' #http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
	file_meta.MediaStorageSOPInstanceUID = "1.2.246.352.81.3.273720375.51644.19651.179.0"
	file_meta.ImplementationClassUID = "1.2.246.352.70.2.1.160.3"

	#Criando um dataset "vazio" ==> https://pydicom.github.io/pydicom/dev/reference/generated/pydicom.dataset.FileDataset.html
	ds = FileDataset(filename_little_endian, {}, file_meta = file_meta, preamble = b"\0"*128)

	#Adicionando elementos
	ds.PatientName = "Teste"
	ds.PatientID = "123456789"

	#Transfer Syntax
	ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
	ds.is_little_endian = True
	ds.is_implicit_VR = False

	#Adicionando data e hora de criação
	dt = datetime.datetime.now()
	ds.ContentDate = dt.strftime('%Y%m%d')
	timeStr = dt.strftime('%H%M%S.%f') # formato longo com micro segundos
	ds.ContentTime = timeStr

	#Carregando arquivo TIFF
	tiff_file = Image.open(nome_tiff)
	#tiff_rotacionada90 = tiff_file.rotate(90)
	#tiff_array = np.array(tiff_rotacionada90)
	tiff_array = np.array(tiff_file)

	#Adicionando array e outras informações da imagem ao dataset
	ds.PixelData = tiff_array.tobytes()

	tiff_meta_dict = {TAGS[key] : tiff_file.tag[key] for key in tiff_file.tag.keys()}

	dpmm = (1/x_res)*sid/sad #pontos por mm no isocentro
	translacao = [translacao[0]*dpmm,translacao[1]*dpmm] # deslocamento em pixel no painel
	
	ds.add_new([0x0008,0x0016], 'UI','1.2.840.10008.5.1.4.1.1.481.1') #SOP Class UID
	ds.add_new([0x0008,0x0018], 'UI','1.2.246.352.81.3.273720375.51644.19651.179.0') #SOP Instance UID
	ds.add_new([0x0028,0x0010], 'US',tiff_meta_dict['ImageLength'][0]) #rows
	ds.add_new([0x0028,0x0011], 'US',tiff_meta_dict['ImageWidth'][0]) #columns
	ds.add_new([0x0028,0x0100], 'US',tiff_meta_dict['BitsPerSample'][0]) #Bits Alocated
	ds.add_new([0x0028,0x0103], 'US', 0) # PixelRepresentation
	ds.add_new([0x0028,0x0002], 'US', tiff_meta_dict['SamplesPerPixel'][0]) # SamplesPerPixel
	ds.add_new([0x0028,0x0004], 'CS', 'MONOCHROME2') # Photometric Interpretation ==> https://dicom.innolitics.com/ciods/enhanced-mr-image/enhanced-mr-image/00280103
	ds.add_new([0x0008,0x0060], 'CS', 'RTIMAGE') #Modality
	ds.add_new([0x0028,0x0101], 'US',tiff_meta_dict['BitsPerSample'][0]) #Bits Stored
	ds.add_new([0x3002,0x0022], 'DS', 1000.0) # Radiation Machine SAD
	ds.add_new([0x3002,0x0026], 'DS', 1600.0) # RT Image SID
	ds.add_new([0x5000,0x0030], 'SH', ['PIXL', 'PIXL']) #Axis Units
	ds.add_new([0x3002,0x0011], 'DS', [x_res,x_res]) #Image Plane Pixel Spacing
	ds.add_new([0x3002,0x000D], 'DS', translacao) # X-Ray Image Receptor Translation Attribute ==> https://dicom.innolitics.com/ciods/rt-beams-delivery-instruction/rt-beams-delivery-instruction/00741020/00741030/3002000d
	ds.add_new([0x300A,0x011E], 'DS', gantry)# Gantry Angle
	ds.add_new([0x300A,0x0120], 'DS', colimador)# Beam Limiting Device (Colimator) Angle
	
	ds.save_as(nome_dicom)
	#print(nome_dicom)

	#print('Pronto!')
	#plt.imshow(ds.pixel_array)
	#plt.show()
	#print(ds)

#def picketfence(nome_tiff, nome_dicom, translacao, sad, sid):
#	convert(nome_tiff, nome_dicom, translacao, sad, sid)

def get_dicom():
	return ds

def save_dicom(nome_dicom):
	ds.save_as(nome_dicom)
	print('Pronto!')
