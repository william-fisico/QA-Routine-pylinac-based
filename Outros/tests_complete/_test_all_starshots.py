"""Travis CI memory can't handle all the starshots; thus only test them when explicitly asked to."""
import os.path as osp
from unittest import TestCase

from tests_basic.test_starshot import StarMixin, Point

from tests_basic import TEST_BANK_DIR


class StarBankMixin(StarMixin):
    dir_location = osp.join(TEST_BANK_DIR, 'Starshots')


class Starshot2(StarBankMixin, TestCase):
    file_path = ['Starshot#2.tif']
    wobble_center = Point(566, 590)
    wobble_diameter_mm = 0.2
    num_rad_lines = 4
    # outside: 0.18-0.19


class Starshot3(StarBankMixin, TestCase):
    file_path = ['Starshot#3.tif']
    wobble_center = Point(466, 595)
    wobble_diameter_mm = 0.32
    num_rad_lines = 6
    # outside 0.33


class Starshot4(StarBankMixin, TestCase):
    file_path = ['Starshot#4.tif']
    wobble_center = Point(446, 565)
    wobble_diameter_mm = 0.38
    num_rad_lines = 6
    # outside 0.39


class Starshot5(StarBankMixin, TestCase):
    file_path = ['Starshot#5.tif']
    wobble_center = Point(557, 580)
    wobble_diameter_mm = 0.15
    num_rad_lines = 4
    wobble_tolerance = 0.2
    # outside: 0.14


class Starshot6(StarBankMixin, TestCase):
    file_path = ['Starshot#6.tif']
    wobble_center = Point(528, 607)
    wobble_diameter_mm = 0.3
    num_rad_lines = 7


class Starshot7(StarBankMixin, TestCase):
    file_path = ['Starshot#7.tif']
    wobble_center = Point(469, 646)
    wobble_diameter_mm = 0.2
    num_rad_lines = 4
    wobble_tolerance = 0.2


class Starshot8(StarBankMixin, TestCase):
    file_path = ['Starshot#8.tiff']
    wobble_center = Point(686, 669)
    wobble_diameter_mm = 0.35
    num_rad_lines = 5


class Starshot9(StarBankMixin, TestCase):
    file_path = ['Starshot#9.tiff']
    wobble_center = Point(714, 611)
    wobble_diameter_mm = 0.3
    num_rad_lines = 5


class Starshot10(StarBankMixin, TestCase):
    file_path = ['Starshot#10.tiff']
    wobble_center = Point(725, 802)
    wobble_diameter_mm = 0.65
    num_rad_lines = 5


class Starshot11(StarBankMixin, TestCase):
    file_path = ['Starshot#11.tiff']
    wobble_center = Point(760, 650)
    wobble_diameter_mm = 0.6
    num_rad_lines = 4


class Starshot12(StarBankMixin, TestCase):
    file_path = ['Starshot#12.tiff']
    wobble_center = Point(315, 292)
    wobble_diameter_mm = 0.88
    num_rad_lines = 4


class Starshot13(StarBankMixin, TestCase):
    file_path = ['Starshot#13.tiff']
    wobble_center = Point(376, 303)
    wobble_diameter_mm = 0.2
    num_rad_lines = 4


class Starshot14(StarBankMixin, TestCase):
    file_path = ['Starshot#14.tiff']
    wobble_center = Point(334, 282)
    wobble_diameter_mm = 0.55
    num_rad_lines = 4


class Starshot15(StarBankMixin, TestCase):
    file_path = ['Starshot#15.tiff']
    wobble_center = Point(346, 309)
    wobble_diameter_mm = 0.6
    num_rad_lines = 4


class Starshot16(StarBankMixin, TestCase):
    file_path = ['Starshot#16.tiff']
    wobble_center = Point(1444, 1452)
    wobble_diameter_mm = 0.6
    num_rad_lines = 6


class Starshot17(StarBankMixin, TestCase):
    file_path = ['Starshot#17.tiff']
    wobble_center = Point(1475, 1361)
    wobble_diameter_mm = 0.44
    num_rad_lines = 6


class Starshot18(StarBankMixin, TestCase):
    file_path = ['Starshot#18.tiff']
    wobble_center = Point(1516, 1214)
    wobble_diameter_mm = 0.6
    num_rad_lines = 6


class Starshot19(StarBankMixin, TestCase):
    file_path = ['Starshot#19.tiff']
    wobble_center = Point(1475, 1276)
    wobble_diameter_mm = 0.6
    num_rad_lines = 6


class Starshot20(StarBankMixin, TestCase):
    file_path = ['Starshot#20.tiff']
    wobble_center = Point(347, 328)
    wobble_diameter_mm = 0.75
    num_rad_lines = 4


class Starshot21(StarBankMixin, TestCase):
    file_path = ['Starshot#21.tiff']
    wobble_center = Point(354, 294)
    wobble_diameter_mm = 1.3
    wobble_tolerance = 0.2
    num_rad_lines = 4
    passes = False


class Starshot22(StarBankMixin, TestCase):
    file_path = ['Starshot#22.tiff']
    wobble_center = Point(1305, 1513)
    wobble_diameter_mm = 0.9
    num_rad_lines = 9
    # outside 0.93mm

    def test_bad_input_no_recursion_fails(self):
        """Test that without recursion, a bad setup fails."""
        with self.assertRaises(RuntimeError):
            self.star.analyze(radius=0.3, min_peak_height=0.95, recursive=False)

        # but will pass with recursion
        self.star.analyze()
        self.test_passed()


class Starshot23(StarBankMixin, TestCase):
    file_path = ['Starshot#23.tiff']
    wobble_center = Point(1297, 1699)
    wobble_diameter_mm = 0.38
    num_rad_lines = 9


class Starshot24(StarBankMixin, TestCase):
    file_path = ['Starshot#24.tiff']
    wobble_center = Point(1370, 1454)
    wobble_diameter_mm = 0.3
    num_rad_lines = 4


class Starshot25(StarBankMixin, TestCase):
    file_path = ['Starshot#25.tiff']
    wobble_center = Point(286, 279)
    wobble_diameter_mm = 0.3
    num_rad_lines = 4


class Starshot26(StarBankMixin, TestCase):
    file_path = ['Starshot#26.tiff']
    wobble_center = Point(1511, 1452)
    wobble_diameter_mm = 0.55
    num_rad_lines = 4
    wobble_tolerance = 0.15


class Starshot27(StarBankMixin, TestCase):
    file_path = ['Starshot#27.tiff']
    wobble_center = Point(1105, 1306)
    wobble_diameter_mm = 0.4
    num_rad_lines = 6


class CRStarshot(StarBankMixin, TestCase):
    file_path = ['CR-Starshot.dcm']
    wobble_center = Point(1030.5, 1253.6)
    wobble_diameter_mm = 0.3
    num_rad_lines = 6


class ChicagoSet(StarBankMixin, TestCase):
    file_path = ['Chicago']
    wobble_center = Point(638, 639.3)
    wobble_diameter_mm = 0.65
    num_rad_lines = 5
    is_dir = True
