import glob
import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import generate_uid

list_files = glob.glob('./*.dcm')
for f in list_files:
	ds = pydicom.filereader.read_file(f)
	print(f)
	print(ds)
	print('*************************')