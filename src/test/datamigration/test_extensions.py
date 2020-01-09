import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile, NWBHDF5IO
from pynwb.device import Device

from src.datamigration.extension.probe import Probe

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())


class TestExtensions(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.content = NWBFile(session_description='metadata.session_description',
                               experimenter='metadata.experimenter_name',
                               lab='metadata.lab',
                               institution='metadata.institution',
                               session_start_time=start_time,
                               identifier=str('metadata.identifier'),
                               experiment_description='metadata.experiment_description',
                               electrode_groups=[Probe(id=6,
                                                       probe_type='probiusz typ',
                                                       electrode_groups=[1, 2, 3],
                                                       ntrodes=[5, 5, 5],
                                                       contact_size=4.5,
                                                       num_shanks=4,
                                                       name='EGname',
                                                       description='byly sobie swinki trzy',
                                                       location='krakow',
                                                       device=Device(name='trodes'),
                                                       )
                                                 ]
                               )
        with NWBHDF5IO(path='output_file.nwb', mode='w') as nwb_fileIO:
            nwb_fileIO.write(self.content)
            nwb_fileIO.close()

    def test_probe_creation(self):
        nwb_file = NWBHDF5IO('example_file_path.nwb', 'r')
        nwbfile_read = nwb_file.read()
        self.assertEqual('probiusz typ', nwbfile_read.electrode_groups)
        self.assertEqual(self.probe.name, return_probe.name)
        self.assertEqual(self.probe.device_name, return_probe.device_name)
        self.assertEqual(self.probe.probe_description, return_probe.probe_description)
