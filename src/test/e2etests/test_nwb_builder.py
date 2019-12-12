import os
import unittest

from pynwb import NWBHDF5IO

from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_file_builder import NWBFileBuilder
from src.test.e2etests.experiment_data import ExperimentData

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip("Need NWBFile")
class TestNWBElementBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.output_name = path + '../../output.nwb'
        cls.xml_path = 'datamigration/res/fl_lab_sample_header.xml'
        cls.xml_group = Header(cls.xml_path).configuration.spike_configuration.spike_n_trodes
        cls.metadata = MetadataExtractor(config_path=path + '../../datamigration/res/metadata.yml')

        cls.nwbBuilder = NWBFileBuilder(
            data_path=ExperimentData.root_path,
            animal_name='beans',
            date='20190718',
            dataset='01_s1',
            config_path='datamigration/res/metadata.yml',
            header_path='datamigration/res/fl_lab_sample_header.xml'
        )
        content = cls.nwbBuilder.build()
        cls.nwbBuilder.write(content)

    def test_read_nwb_file(self):
        with NWBHDF5IO(path=self.output_name, mode='r') as io:
            nwb_file = io.read()
            print(nwb_file)
            print('Details: ')
            print('Position: ' + str(nwb_file.processing['position'].data_interfaces['Position']))
            print('Task: ' + str(nwb_file.processing['task'].data_interfaces['novela task']))
            print('Apparatus: ' + str(nwb_file.processing['apparatus'].data_interfaces['apparatus']))
            print(nwb_file.electrodes)

    def test_read_electrodes(self):
        with NWBHDF5IO(path=self.output_name, mode='r') as io:
            nwb_file = io.read()
            electrodes_len = len(nwb_file.electrodes)
            x = []
            y = []
            z = []
            imp = []
            location = []
            filtering = []
            group = []
            electrode_ide = []
            maxDisp = []
            thresh = []
            hwChan = []
            triggerOn = []

            for i in range(electrodes_len):
                x.append(nwb_file.electrodes['x'][i])
                y.append(nwb_file.electrodes['y'][i])
                z.append(nwb_file.electrodes['z'][i])
                imp.append(nwb_file.electrodes['imp'][i])
                location.append(nwb_file.electrodes['location'][i])
                filtering.append(nwb_file.electrodes['filtering'][i])
                group.append(nwb_file.electrodes['group'][i])
                electrode_ide.append(nwb_file.electrodes.id[i])
                maxDisp.append(nwb_file.electrodes['maxDisp'][i])
                thresh.append(nwb_file.electrodes['thresh'][i])
                hwChan.append(nwb_file.electrodes['hwChan'][i])
                triggerOn.append(nwb_file.electrodes['triggerOn'][i])

            print(x)
            print(y)
            print(z)
            print(imp)
            print(location)
            print(filtering)
            print(group)
            print(electrode_ide)
            print(maxDisp)
            print(thresh)
            print(hwChan)
            print(triggerOn)

    def test_check_electrode_groups(self):
        with NWBHDF5IO(path=self.output_name, mode='r') as io:
            nwb_file = io.read()

            electrode_group_0 = nwb_file.electrode_groups['electrode group 1']
            electrode_group_1 = nwb_file.electrode_groups['electrode group 2']

            xml_electrode_group_0 = self.xml_group[0]
            xml_electrode_group_1 = self.xml_group[1]

            metadata_electrode_group_index_0 = 0
            metadata_electrode_group_index_1 = 1

            self.assert_electrode_group(nwb_file, electrode_group_0, metadata_electrode_group_index_0,
                                        xml_electrode_group_0)
            self.assert_electrode_group(nwb_file, electrode_group_1, metadata_electrode_group_index_1,
                                        xml_electrode_group_1)

    def test_check_electrodes(self):
        with NWBHDF5IO(path=self.output_name, mode='r') as io:
            nwb_file = io.read()

            xml_electrodes_0 = self.xml_group[0].spike_channels[0]
            xml_electrodes_1 = self.xml_group[0].spike_channels[1]
            xml_electrodes_2 = self.xml_group[1].spike_channels[0]
            xml_electrodes_3 = self.xml_group[1].spike_channels[1]

            electrode_index_0 = 0
            electrode_index_1 = 1
            electrode_index_2 = 2
            electrode_index_3 = 3

            electrode_metadata_index_0 = 0
            electrode_metadata_index_1 = 1
            electrode_metadata_index_2 = 2
            electrode_metadata_index_3 = 3

            self.assert_electrode(nwb_file, electrode_index_0, electrode_metadata_index_0, xml_electrodes_0)
            self.assert_electrode(nwb_file, electrode_index_1, electrode_metadata_index_1, xml_electrodes_1)
            self.assert_electrode(nwb_file, electrode_index_2, electrode_metadata_index_2, xml_electrodes_2)
            self.assert_electrode(nwb_file, electrode_index_3, electrode_metadata_index_3, xml_electrodes_3)

    def assert_electrode_group(self, nwb_file, electrode_group, metadata_electrode_group_index, xml_electrode_group):
        self.assertEqual(electrode_group.name, self.metadata.electrode_groups[metadata_electrode_group_index]['name'])
        self.assertEqual(electrode_group.description,
                         self.metadata.electrode_groups[metadata_electrode_group_index]['description'])
        self.assertEqual(electrode_group.location,
                         self.metadata.electrode_groups[metadata_electrode_group_index]['location'])
        self.assertEqual(electrode_group.device,
                         nwb_file.devices[self.metadata.electrode_groups[metadata_electrode_group_index]['device']])
        self.assertEqual(electrode_group.filterOn, xml_electrode_group.filter_on)
        self.assertEqual(electrode_group.lowFilter, xml_electrode_group.low_filter)
        self.assertEqual(electrode_group.lfpRefOn, xml_electrode_group.lfp_ref_on)
        self.assertEqual(electrode_group.color, xml_electrode_group.color)
        self.assertEqual(electrode_group.highFilter, xml_electrode_group.hight_filter)
        self.assertEqual(electrode_group.lfpFilterOn, xml_electrode_group.lfp_filter_on)
        self.assertEqual(electrode_group.moduleDataOn, xml_electrode_group.module_data_on)
        self.assertEqual(electrode_group.LFPHighFilter, xml_electrode_group.lfp_high_filter)
        self.assertEqual(electrode_group.refGroup, xml_electrode_group.ref_group)
        self.assertEqual(electrode_group.LFPChan, xml_electrode_group.lfp_chan)
        self.assertEqual(electrode_group.refNTrodeID, xml_electrode_group.ref_n_trode_id)
        self.assertEqual(electrode_group.refChan, xml_electrode_group.ref_chan)
        self.assertEqual(electrode_group.groupRefOn, xml_electrode_group.group_ref_on)
        self.assertEqual(electrode_group.refOn, xml_electrode_group.ref_on)
        self.assertEqual(electrode_group.id, xml_electrode_group.id)

    def assert_electrode(self, nwb_file, electrode_index, metadata_electrodes_index, xml_electrode):
        self.assertEqual(nwb_file.electrodes['x'][electrode_index],
                         self.metadata.electrodes[metadata_electrodes_index]['x'])
        self.assertEqual(nwb_file.electrodes['y'][electrode_index],
                         self.metadata.electrodes[metadata_electrodes_index]['y'])
        self.assertEqual(nwb_file.electrodes['z'][electrode_index],
                         self.metadata.electrodes[metadata_electrodes_index]['z'])
        self.assertEqual(nwb_file.electrodes['imp'][electrode_index],
                         self.metadata.electrodes[metadata_electrodes_index]['imp'])
        self.assertEqual(nwb_file.electrodes['location'][electrode_index],
                         self.metadata.electrodes[metadata_electrodes_index]['location'])
        self.assertEqual(nwb_file.electrodes['filtering'][electrode_index],
                         self.metadata.electrodes[metadata_electrodes_index]['filtering'])
        self.assertEqual(nwb_file.electrodes['group'][electrode_index],
                         nwb_file.electrode_groups[self.metadata.electrodes[metadata_electrodes_index]['group']])
        self.assertEqual(nwb_file.electrodes.id[electrode_index],
                         self.metadata.electrodes[metadata_electrodes_index]['id'])
        self.assertEqual(nwb_file.electrodes['hwChan'][electrode_index], xml_electrode.hw_chan)
        self.assertEqual(nwb_file.electrodes['maxDisp'][electrode_index], xml_electrode.max_disp)
        self.assertEqual(nwb_file.electrodes['thresh'][electrode_index], xml_electrode.thresh)
        self.assertEqual(nwb_file.electrodes['triggerOn'][electrode_index], xml_electrode.trigger_on)

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile('output.nwb'):
            os.remove('output.nwb')
