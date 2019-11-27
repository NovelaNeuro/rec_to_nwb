from datetime import datetime
import unittest
from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.datamigration.extension.probe import Probe
from src.datamigration.extension.shank import Shank

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
create_date = datetime(2017, 4, 15, 12, tzinfo=tzlocal())

class TestExtensions(unittest.TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(session_description='demonstrate external files',
                           identifier='NWBE1',
                           session_start_time=start_time,
                           file_create_date=create_date)

        self.probe = Probe(name='Probe1', probe_id='1')
        self.nwb_file.add_device(self.probe)
        self.shank = Shank(
            name='Shank1',
            description='sample description',
            location='sample location',
            device=self.probe,
            filterOn='filter on',
            lowFilter='low filter',
            lfpRefOn='lfp_ref_on',
            color='color',
            highFilter='hight_filter',
            lfpFilterOn='lfp_filter_on',
            moduleDataOn='module_data_on',
            LFPHighFilter='lfp_high_filter',
            refGroup='ref_group',
            LFPChan='lfp_chan',
            refNTrodeID='ref_n_trode_id',
            refChan='ref_chan',
            groupRefOn='group_ref_on',
            refOn='ref_on',
            id='id')

    def test_probe_creation(self):
        return_probe = self.nwb_file.get_device(name='Probe1')
        self.assertEqual(self.probe, return_probe)
        self.assertEqual(self.probe.name, return_probe.name)
        self.assertEqual(self.probe.probe_id, return_probe.probe_id)

    def test_shank_creation(self):
        self.nwb_file.add_electrode_group(self.shank)
        return_shank = self.nwb_file.get_electrode_group(name='Shank1')

        self.assertEqual(self.shank, return_shank)
        self.assertEqual(self.shank.name, return_shank.name)
        self.assertEqual(self.shank.description, return_shank.description)
        self.assertEqual(self.shank.location, return_shank.location)
        self.assertEqual(self.shank.device, return_shank.device)
        self.assertEqual(self.shank.filterOn, return_shank.filterOn)
        self.assertEqual(self.shank.lowFilter, return_shank.lowFilter)
        self.assertEqual(self.shank.lfpRefOn, return_shank.lfpRefOn)
        self.assertEqual(self.shank.color, return_shank.color)
        self.assertEqual(self.shank.highFilter, return_shank.highFilter)
        self.assertEqual(self.shank.lfpFilterOn, return_shank.lfpFilterOn)
        self.assertEqual(self.shank.moduleDataOn, return_shank.moduleDataOn)
        self.assertEqual(self.shank.LFPHighFilter, return_shank.LFPHighFilter)
        self.assertEqual(self.shank.refGroup, return_shank.refGroup)
        self.assertEqual(self.shank.LFPChan, return_shank.LFPChan)
        self.assertEqual(self.shank.refNTrodeID, return_shank.refNTrodeID)
        self.assertEqual(self.shank.refChan, return_shank.refChan)
        self.assertEqual(self.shank.groupRefOn, return_shank.groupRefOn)
        self.assertEqual(self.shank.refOn, return_shank.refOn)
        self.assertEqual(self.shank.id, return_shank.id)
