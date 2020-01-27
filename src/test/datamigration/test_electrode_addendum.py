import unittest

from src.datamigration.nwb_builder.electrode_addentum import ElectrodeAddendum


class TestElectrodeAddendum(unittest.TestCase):

    def setUp(self):
        self.electrode_addendum = ElectrodeAddendum()
        self.rel_x_test = [1, 2, 3]
        self.rel_y_test = [4, 5, 6]
        self.rel_z_test = [7, 8, 9]
        self.electrode_counter = 10


        self.electrode_addendum.rel_x.extend(self.rel_x_test)
        self.electrode_addendum.rel_y.extend(self.rel_y_test)
        self.electrode_addendum.rel_z.extend(self.rel_z_test)
        self.electrode_addendum.electrode_counter = self.electrode_counter

    def test_electrode_addendum(self):
        self.assertEqual(self.electrode_addendum.rel_x, self.rel_x_test)
        self.assertEqual(self.electrode_addendum.rel_y, self.rel_y_test)
        self.assertEqual(self.electrode_addendum.rel_z, self.rel_z_test)
        self.assertEqual(self.electrode_addendum.electrode_counter, self.electrode_counter)
