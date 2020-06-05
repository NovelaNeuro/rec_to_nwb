import os
from unittest import TestCase
from unittest.mock import Mock
from testfixtures import should_raise

from ndx_franklab_novela.probe import Shank

from rec_to_nwb.processing.nwb.components.device.probe.fl_probe import FlProbe
from rec_to_nwb.processing.nwb.components.device.probe.fl_probe_manager import FlProbeManager

path = os.path.dirname(os.path.abspath(__file__))


class TestFlProbeManager(TestCase):

    def setUp(self):
        self.probes_metadata_1 = {
            'probe_type': 'tetrode_12.5', 'contact_size': 20.0, 'units': 'um',
            'probe_description': 'sample description 1', 'contact_side_numbering': True,
            'shanks': [
                {'shank_id': 0, 'electrodes': [
                    {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                    {'id': 1, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                ]}]}
        self.probes_metadata_2 = {
            'probe_type': '128c-4s8mm6cm-20um-40um-sl', 'contact_size': 20.0, 'units': 'mm',
            'probe_description': 'sample description 2', 'contact_side_numbering': False,
            'shanks': [
                {'shank_id': 0, 'electrodes': [
                    {'id': 0, 'rel_x': 0.0, 'rel_y': 0.0, 'rel_z': 0.0},
                    {'id': 1, 'rel_x': 40.0, 'rel_y': 0.0, 'rel_z': 0.0}]},
                {'shank_id': 1, 'electrodes': [
                    {'id': 32, 'rel_x': 0.0, 'rel_y': 300.0, 'rel_z': 0.0},
                    {'id': 33, 'rel_x': 40.0, 'rel_y': 300.0, 'rel_z': 0.0}]},
                {'shank_id': 2, 'electrodes': [
                    {'id': 64, 'rel_x': 0.0, 'rel_y': 600.0, 'rel_z': 0.0},
                    {'id': 65, 'rel_x': 40.0, 'rel_y': 600.0, 'rel_z': 0.0}, ]},
            ]}
        self.probes_metadata = [self.probes_metadata_1, self.probes_metadata_2]

    def test_manager_builds_FlProbes_successfully(self):
        mock_shank_1 = Mock(spec=Shank)
        mock_shank_2 = Mock(spec=Shank)
        mock_shank_3 = Mock(spec=Shank)
        mock_shank_4 = Mock(spec=Shank)
        mock_shank_5 = Mock(spec=Shank)
        mock_shank_6 = Mock(spec=Shank)

        mock_shanks_dict = {
            'tetrode_12.5': [mock_shank_1, mock_shank_2],
            '128c-4s8mm6cm-20um-40um-sl': [mock_shank_1, mock_shank_2,
                                           mock_shank_3, mock_shank_4,
                                           mock_shank_5, mock_shank_6]
        }

        probes_valid_map = {'128c-4s8mm6cm-20um-40um-sl'}

        fl_probe_manager = FlProbeManager(
            probes_metadata=self.probes_metadata,
        )
        fl_probes = fl_probe_manager.get_fl_probes(
            shanks_dict=mock_shanks_dict,
            probes_valid_map=probes_valid_map
        )

        self.assertIsInstance(fl_probes[0], FlProbe)
        self.assertIsInstance(fl_probes[0].probe_id, int)
        self.assertIsInstance(fl_probes[0].name, str)
        self.assertIsInstance(fl_probes[0].probe_type, str)
        self.assertIsInstance(fl_probes[0].units, str)
        self.assertIsInstance(fl_probes[0].probe_description, str)
        self.assertIsInstance(fl_probes[0].contact_size, float)
        self.assertIsInstance(fl_probes[0].shanks, list)

        self.assertEqual(len(fl_probes[0].shanks), 6)

        self.assertEqual(fl_probes[0].probe_id, 0)
        self.assertEqual(fl_probes[0].name, 'probe 0')
        self.assertEqual(fl_probes[0].probe_type, '128c-4s8mm6cm-20um-40um-sl')
        self.assertEqual(fl_probes[0].units, 'mm')
        self.assertEqual(fl_probes[0].probe_description, 'sample description 2')
        self.assertEqual(fl_probes[0].contact_size, 20.0)
        self.assertEqual(fl_probes[0].shanks, [mock_shank_1, mock_shank_2,
                                               mock_shank_3, mock_shank_4,
                                               mock_shank_5, mock_shank_6]
                         )

    @should_raise(TypeError)
    def test_manager_fails_due_to_None_param(self):
        FlProbeManager(
            probes_metadata=None
        )

    @should_raise(TypeError)
    def test_manager_fails_creating_FlProbes_due_to_None_param(self):
        fl_probe_manager = FlProbeManager(
            probes_metadata=self.probes_metadata
        )

        fl_probe_manager.get_fl_probes(None, None)
