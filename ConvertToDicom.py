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
from pydicom.uid import generate_uid
from PIL import Image
from PIL.TiffTags import TAGS
import numpy as np
import matplotlib.pyplot as plt

def convert(nome_paciente, id_paciente, nome_tiff, nome_dicom, translacao, sad, sid, gantry, colimador, x_res):
	global ds
	# Nome do arquivo
	filename_little_endian = nome_dicom

	#https://pydicom.github.io/pynetdicom/dev/user/concepts.html
	#https://pydicom.github.io/pydicom/dev/reference/generated/pydicom.uid.generate_uid.html
	#https://www.medicalconnections.co.uk/FreeUID/
	instance_uid = generate_uid(prefix='1.2.826.0.1.3680043.10.565.')

	# Criando arquivos com informações minimas
	#print('Criando arquivo Dicom Image')
	file_meta = FileMetaDataset()
	file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.1' #http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
	file_meta.MediaStorageSOPInstanceUID = instance_uid

	#Criando um dataset "vazio" ==> https://pydicom.github.io/pydicom/dev/reference/generated/pydicom.dataset.FileDataset.html
	ds = FileDataset(filename_little_endian, {}, file_meta = file_meta, preamble = b"\0"*128)

	#Adicionando elementos
	ds.PatientName = nome_dicom
	ds.PatientID = id_paciente

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
	ds.add_new([0x0008,0x0018], 'UI',instance_uid) #SOP Instance UID
	ds.add_new([0x0028,0x0010], 'US',tiff_meta_dict['ImageLength'][0]) #rows
	ds.add_new([0x0028,0x0011], 'US',tiff_meta_dict['ImageWidth'][0]) #columns
	ds.add_new([0x0028,0x0100], 'US',tiff_meta_dict['BitsPerSample'][0]) #Bits Alocated
	ds.add_new([0x0028,0x0103], 'US', 0) # PixelRepresentation
	ds.add_new([0x0028,0x0002], 'US', tiff_meta_dict['SamplesPerPixel'][0]) # SamplesPerPixel
	ds.add_new([0x0028,0x0004], 'CS', 'MONOCHROME2') # Photometric Interpretation ==> https://dicom.innolitics.com/ciods/enhanced-mr-image/enhanced-mr-image/00280103
	ds.add_new([0x0008,0x0060], 'CS', 'RTIMAGE') #Modality
	ds.add_new([0x0028,0x0101], 'US',tiff_meta_dict['BitsPerSample'][0]) #Bits Stored
	ds.add_new([0x0028,0x0102], 'US',tiff_meta_dict['BitsPerSample'][0]-1) #High Bit ==> https://dicom.innolitics.com/ciods/us-image/image-pixel/00280102
	ds.add_new([0x3002,0x0022], 'DS', sad) # Radiation Machine SAD
	ds.add_new([0x3002,0x0026], 'DS', sid) # RT Image SID
	ds.add_new([0x5000,0x0030], 'SH', ['PIXL', 'PIXL']) #Axis Units
	ds.add_new([0x3002,0x0011], 'DS', [x_res,x_res]) #Image Plane Pixel Spacing
	ds.add_new([0x3002,0x000D], 'DS', translacao) # X-Ray Image Receptor Translation Attribute ==> https://dicom.innolitics.com/ciods/rt-beams-delivery-instruction/rt-beams-delivery-instruction/00741020/00741030/3002000d
	ds.add_new([0x300A,0x011E], 'DS', gantry)# Gantry Angle
	ds.add_new([0x300A,0x0120], 'DS', colimador)# Beam Limiting Device (Colimator) Angle
	
	ds.save_as(nome_dicom)


def get_dicom():
	return ds

def save_dicom(nome_dicom):
	ds.save_as(nome_dicom)
	print('Pronto!')
