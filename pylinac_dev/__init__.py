
import sys

__version__ = '2.3.2'
__version_info__ = (2, 3, 2)

# check python version
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    raise ValueError("pylinac_dev is only supported on Python 3.6+. Please update your environment.")

# import shortcuts
from pylinac_dev.ct import CatPhan504, CatPhan600, CatPhan503, CatPhan604
from pylinac_dev.core import decorators, geometry, image, io, mask, profile, roi, utilities
from pylinac_dev.core.utilities import clear_data_files, assign2machine
from pylinac_dev.flatsym import FlatSym
from pylinac_dev.planar_imaging import LeedsTOR, StandardImagingQC3, LasVegas, DoselabMC2kV, DoselabMC2MV
from pylinac_dev.log_analyzer import load_log, Dynalog, TrajectoryLog, MachineLogs
from pylinac_dev.picketfence import PicketFence  # must be after log analyzer
from pylinac_dev.starshot import Starshot
from pylinac_dev.vmat import DRMLC, DRGS
from pylinac_dev.winston_lutz import WinstonLutz
from pylinac_dev.calibration import tg51, trs398

from pylinac_dev.watcher import process
