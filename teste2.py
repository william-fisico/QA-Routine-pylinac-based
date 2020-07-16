from pylinac_dev import PicketFence
import ConvertToDicom
import matplotlib.pyplot as plt
import pydicom
import numpy as np

x = "EPID-PF-LR.dcm"
ds = pydicom.filereader.read_file("G0C0Y2_teste.dcm")
try:
	print("gantry",ds[0x3002,0x000D])
	print(ds[0x3002,0x000D].value)
except:
	print(0)
'''

Dataset.file_meta -------------------------------
(0002, 0000) File Meta Information Group Length  UL: 206
(0002, 0001) File Meta Information Version       OB: b'\x00\x01'
(0002, 0002) Media Storage SOP Class UID         UI: RT Image Storage
(0002, 0003) Media Storage SOP Instance UID      UI: 1.2.840.113854.197903946100000859336331322181886994139.1.1
(0002, 0010) Transfer Syntax UID                 UI: Implicit VR Little Endian
(0002, 0012) Implementation Class UID            UI: 1.2.826.0.1.3680043.2.135.1066.101
(0002, 0013) Implementation Version Name         SH: '1.4.16/WIN32'
-------------------------------------------------
(0008, 0000) Group Length                        UL: 366
(0008, 0008) Image Type                          CS: ['DERIVED', 'SECONDARY', 'PORTAL']
(0008, 0016) SOP Class UID                       UI: RT Image Storage
(0008, 0018) SOP Instance UID                    UI: 1.2.840.113854.197903946100000859336331322181886994139.1.1
(0008, 0020) Study Date                          DA: '20141111'
(0008, 0023) Content Date                        DA: '20141111'
(0008, 0030) Study Time                          TM: '172150'
(0008, 0033) Content Time                        TM: '172150'
(0008, 0050) Accession Number                    SH: ''
(0008, 0060) Modality                            CS: 'RTIMAGE'
(0008, 0064) Conversion Type                     CS: 'WSD'
(0008, 0070) Manufacturer                        LO: 'IMPAC Medical Systems, Inc.'
(0008, 0090) Referring Physician's Name          PN: ''
(0008, 1030) Study Description                   LO: 'PTV'
(0008, 103e) Series Description                  LO: 'PF 0 + StaticMLC-Y40'
(0008, 1048) Physician(s) of Record              PN: ''
(0008, 1070) Operators' Name                     PN: ''
(0008, 1090) Manufacturer's Model Name           LO: 'MOSAIQ'
(0010, 0000) Group Length                        UL: 54
(0010, 0010) Patient's Name                      PN: 'Moby Dick'
(0010, 0020) Patient ID                          LO: 'Whale'
(0010, 0030) Patient's Birth Date                DA: ''
(0018, 0000) Group Length                        UL: 18
(0018, 1020) Software Versions                   LO: '2.41.01J0'
(0020, 0000) Group Length                        UL: 182
(0020, 000d) Study Instance UID                  UI: 1.2.840.113854.197903946100000859336331322181886994139
(0020, 000e) Series Instance UID                 UI: 1.2.840.113854.197903946100000859336331322181886994139.1
(0020, 0010) Study ID                            SH: '343128'
(0020, 0011) Series Number                       IS: "4442325"
(0020, 0013) Instance Number                     IS: "0"
(0020, 0020) Patient Orientation                 CS: ''
(0020, 1040) Position Reference Indicator        LO: ''
(0028, 0000) Group Length                        UL: 90
(0028, 0002) Samples per Pixel                   US: 1
(0028, 0004) Photometric Interpretation          CS: 'MONOCHROME2'
(0028, 0010) Rows                                US: 768
(0028, 0011) Columns                             US: 1024
(0028, 0100) Bits Allocated                      US: 16
(0028, 0101) Bits Stored                         US: 16
(0028, 0102) High Bit                            US: 15
(0028, 0103) Pixel Representation                US: 0
(3002, 0000) Group Length                        UL: 88
(3002, 0002) RT Image Label                      SH: 'PF 0'
(3002, 000c) RT Image Plane                      CS: 'NORMAL'
(3002, 000e) X-Ray Image Receptor Angle          DS: None
(3002, 0011) Image Plane Pixel Spacing           DS: [0.392, 0.392]
(3002, 0012) RT Image Position                   DS: None
(3002, 0022) Radiation Machine SAD               DS: "1000.0"
(3002, 0026) RT Image SID                        DS: "1000.0"
(300a, 0000) Group Length                        UL: 10
(300a, 00b3) Primary Dosimeter Unit              CS: 'MU'
(5000, 0000) Group Length                        UL: 168
(5000, 0005) Curve Dimensions                    US: 2
(5000, 0010) Number of Points                    US: 4
(5000, 0020) Type of Data                        CS: 'ROI'
(5000, 0022) Curve Description                   LO: ''
(5000, 0030) Axis Units                          SH: ['PIXL', 'PIXL']
(5000, 0103) Data Value Representation           US: 3
(5000, 2500) Curve Label                         LO: 'Field Edge (PF 0:TX)'
(5000, 3000) Curve Data                          OB or OW: Array of 64 elements
(7fe0, 0000) Group Length                        UL: 1572872
(7fe0, 0010) Pixel Data                          OW: Array of 1572864 elements


'''