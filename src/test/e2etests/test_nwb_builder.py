import unittest

from pynwb import NWBHDF5IO

from src.datamigration.header.module.header import Header
from src.datamigration.nwb_file_builder import NWBFileBuilder
from .experiment_data import ExperimentData


class TestNWBBuilder(unittest.TestCase):

    def setUp(self):
        # ToDo I pass path to our sample header due to lack of proper metadata. In sample header we have only 2 records for ElectrodeGroup to fabricate with our sample metadata.yml
        self.output_name = 'output.nwb'
        self.xml_path = 'datamigration/res/fl_lab_sample_header.xml'
        self.xml_group = Header(self.xml_path).configuration.spike_configuration.spike_n_trodes

        self.nwbBuilder = NWBFileBuilder(
            data_path=ExperimentData.root_path,
            animal_name='beans',
            date='20190718',
            dataset='01_s1',
            config_path='datamigration/res/metadata.yml',
            xml_path=self.xml_path,
            output_file_location='',
            output_file_name=self.output_name
        )

    @unittest.skip("Super heavy NWB generation")
    def test_run_nwb_generation_from_preprocessed_data(self):
        nwb_file_path = self.nwbBuilder.build(mda_data_chunk_size=4)
        with NWBHDF5IO(path=nwb_file_path, mode='r') as io:
            nwb_file = io.read()
            print(nwb_file)
            print('Details: ')
            print('Position: ' + str(nwb_file.processing['position'].data_interfaces['Position']))
            print('Task: ' + str(nwb_file.processing['task'].data_interfaces['novela task']))
            print('Apparatus: ' + str(nwb_file.processing['apparatus'].data_interfaces['apparatus']))

            print(nwb_file.electrodes)

    @unittest.skip("No need to read it every time")
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
            id = []
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
                id.append(nwb_file.electrodes.id[i])
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
            print(id)
            print(maxDisp)
            print(thresh)
            print(hwChan)
            print(triggerOn)

    @unittest.skip("Need NWBFile")
    def test_check_electrode_groups(self):
        with NWBHDF5IO(path=self.output_name, mode='r') as io:
            nwb_file = io.read()

            electrodegroup1 = nwb_file.electrode_groups['electrode group 1']
            electrodegroup2 = nwb_file.electrode_groups['electrode group 2']

            xml_electrodegroup1 = self.xml_group[0]
            xml_electrodegroup2 = self.xml_group[1]

            self.assertEqual(electrodegroup1.name, 'electrode group 1')
            self.assertEqual(electrodegroup1.description, 'some description 1')
            self.assertEqual(electrodegroup1.location, 'some location 1')
            self.assertEqual(electrodegroup1.device, nwb_file.devices['dev1'])
            self.assertEqual(electrodegroup1.filterOn, xml_electrodegroup1.filter_on)
            self.assertEqual(electrodegroup1.lowFilter, xml_electrodegroup1.low_filter)
            self.assertEqual(electrodegroup1.lfpRefOn, xml_electrodegroup1.lfp_ref_on)
            self.assertEqual(electrodegroup1.color, xml_electrodegroup1.color)
            self.assertEqual(electrodegroup1.highFilter, xml_electrodegroup1.hight_filter)
            self.assertEqual(electrodegroup1.lfpFilterOn, xml_electrodegroup1.lfp_filter_on)
            self.assertEqual(electrodegroup1.moduleDataOn, xml_electrodegroup1.module_data_on)
            self.assertEqual(electrodegroup1.LFPHighFilter, xml_electrodegroup1.lfp_high_filter)
            self.assertEqual(electrodegroup1.refGroup, xml_electrodegroup1.ref_group)
            self.assertEqual(electrodegroup1.LFPChan, xml_electrodegroup1.lfp_chan)
            self.assertEqual(electrodegroup1.refNTrodeID, xml_electrodegroup1.ref_n_trode_id)
            self.assertEqual(electrodegroup1.refChan, xml_electrodegroup1.ref_chan)
            self.assertEqual(electrodegroup1.groupRefOn, xml_electrodegroup1.group_ref_on)
            self.assertEqual(electrodegroup1.refOn, xml_electrodegroup1.ref_on)
            self.assertEqual(electrodegroup1.id, xml_electrodegroup1.id)

            self.assertEqual(electrodegroup2.name, 'electrode group 2')
            self.assertEqual(electrodegroup2.description, 'some description 2')
            self.assertEqual(electrodegroup2.location, 'some location 2')
            self.assertEqual(electrodegroup2.device, nwb_file.devices['dev2'])
            self.assertEqual(electrodegroup2.filterOn, xml_electrodegroup2.filter_on)
            self.assertEqual(electrodegroup2.lowFilter, xml_electrodegroup2.low_filter)
            self.assertEqual(electrodegroup2.lfpRefOn, xml_electrodegroup2.lfp_ref_on)
            self.assertEqual(electrodegroup2.color, xml_electrodegroup2.color)
            self.assertEqual(electrodegroup2.highFilter, xml_electrodegroup2.hight_filter)
            self.assertEqual(electrodegroup2.lfpFilterOn, xml_electrodegroup2.lfp_filter_on)
            self.assertEqual(electrodegroup2.moduleDataOn, xml_electrodegroup2.module_data_on)
            self.assertEqual(electrodegroup2.LFPHighFilter, xml_electrodegroup2.lfp_high_filter)
            self.assertEqual(electrodegroup2.refGroup, xml_electrodegroup2.ref_group)
            self.assertEqual(electrodegroup2.LFPChan, xml_electrodegroup2.lfp_chan)
            self.assertEqual(electrodegroup2.refNTrodeID, xml_electrodegroup2.ref_n_trode_id)
            self.assertEqual(electrodegroup2.refChan, xml_electrodegroup2.ref_chan)
            self.assertEqual(electrodegroup2.groupRefOn, xml_electrodegroup2.group_ref_on)
            self.assertEqual(electrodegroup2.refOn, xml_electrodegroup2.ref_on)
            self.assertEqual(electrodegroup2.id, xml_electrodegroup2.id)

    @unittest.skip("Need NWBFile")
    def test_check_electrodes(self):
        with NWBHDF5IO(path=self.output_name, mode='r') as io:
            nwb_file = io.read()

            electrode = nwb_file.electrodes

            xml_electrodes1 = self.xml_group[0].spike_channels[0]
            xml_electrodes4 = self.xml_group[1].spike_channels[1]

            self.assertEqual(electrode['x'][0], 1.0)
            self.assertEqual(electrode['y'][0], 1.0)
            self.assertEqual(electrode['z'][0], 1.0)
            self.assertEqual(electrode['imp'][0], 3.0)
            self.assertEqual(electrode['location'][0], 'hippocampus')
            self.assertEqual(electrode['filtering'][0], 'no filter')
            self.assertEqual(electrode['group'][0], nwb_file.electrode_groups['electrode group 1'])
            self.assertEqual(electrode.id[0], 1)
            self.assertEqual(electrode['hwChan'][0], xml_electrodes1.hw_chan)
            self.assertEqual(electrode['maxDisp'][0], xml_electrodes1.max_disp)
            self.assertEqual(electrode['thresh'][0], xml_electrodes1.thresh)
            self.assertEqual(electrode['triggerOn'][0], xml_electrodes1.trigger_on)

            self.assertEqual(electrode['x'][3], 2.0)
            self.assertEqual(electrode['y'][3], 2.0)
            self.assertEqual(electrode['z'][3], 2.0)
            self.assertEqual(electrode['imp'][3], 5.0)
            self.assertEqual(electrode['location'][3], 'neocortex')
            self.assertEqual(electrode['filtering'][3], 'yes filter')
            self.assertEqual(electrode['group'][3], nwb_file.electrode_groups['electrode group 2'])
            self.assertEqual(electrode.id[3], 4)
            self.assertEqual(electrode['hwChan'][3], xml_electrodes4.hw_chan)
            self.assertEqual(electrode['maxDisp'][3], xml_electrodes4.max_disp)
            self.assertEqual(electrode['thresh'][3], xml_electrodes4.thresh)
            self.assertEqual(electrode['triggerOn'][3], xml_electrodes4.trigger_on)
