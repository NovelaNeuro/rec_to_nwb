from unittest import TestCase

from ndx_fllab_novela.probe import ShanksElectrode

from fl.datamigration.nwb.components.device.shanks_electrodes.fl_shanks_electrodes import FlShanksElectrodes


class TestFlShanksElectrodeManager(TestCase):

    def test_fl_shanks_electrode_manager_create_fl_shank_successfully(self):
        metadata = [
            {'shank_id': 0,
             'electrodes': [
                 {'id': 0, 'rel_x': 1, 'rel_y': 2, 'rel_z': 3},
                 {'id': 1, 'rel_x': 11, 'rel_y': 13, 'rel_z': 12},
                ]
             },
            {'shank_id': 1,
             'electrodes': [
                 {'id': 2, 'rel_x': 123, 'rel_y': 7, 'rel_z': 12},
                 {'id': 3, 'rel_x': 5, 'rel_y': 124, 'rel_z': 18},
                 ]
             }
        ]


        fl_shanks_electrode_manager = FlShanksElectrodesManager()
        fl_shanks_elecrodes = fl_shanks_electrode_manager.get_fl_shanks_electrodes()

        self.assertIsInstance(fl_shanks_elecrodes, FlShanksElectrodes)
        self.assertEqual(fl_shanks_elecrodes[0].id, 0)
        self.assertEqual(fl_shanks_elecrodes[0].rel_x, 1)
        self.assertEqual(fl_shanks_elecrodes[0].rel_y, 2)
        self.assertEqual(fl_shanks_elecrodes[0].rel_z, 3)


    def test_fl_shanks_electrode_manager_failed_creating_fl_shank_due_to_None_param(self):
        pass