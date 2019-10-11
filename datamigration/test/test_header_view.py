import unittest

from datamigration.datamigration import xml_header_view


class TestHeaderInterface(unittest.TestCase):

    def setUp(self):
        self.header = xml_header_view.Header(filename='fl_lab_sample_header.xml')

    def test_configuration_tag(self):
        configuration = self.header.get_Configuration()
        self.assertIsNotNone(configuration)
        self.assertEqual('Configuration', configuration.tag)
        self.assertEqual([], configuration.items())
        self.assertEqual(6, len(list(configuration)))

    def test_global_configuration_tag(self):
        global_configuration = self.header.Configuration().get_GlobalConfiguration()
        self.assertIsNotNone(global_configuration)
        self.assertEqual('GlobalConfiguration', global_configuration.tag)
        self.assertEqual(('compileDate', 'May 16 2019'), global_configuration.items()[10])
        self.assertEqual(20, len(global_configuration.items()))
        self.assertEqual(0, len(list(global_configuration)))

    def test_hardware_configuration_tag(self):
        hardware_configuration = self.header.Configuration().get_HardwareConfiguration()
        self.assertIsNotNone(hardware_configuration)
        self.assertEqual('HardwareConfiguration', hardware_configuration.tag)
        self.assertEqual(('samplingRate', '30000'), hardware_configuration.items()[0])
        self.assertEqual(2, len(hardware_configuration.items()))
        self.assertEqual(2, len(list(hardware_configuration)))
        self.assertEqual('Device', list(hardware_configuration)[1].tag)

    def test_device_tag(self):
        device = self.header().HardwareConfiguration().get_Devices()[1]
        self.assertNotEqual([], device)
        self.assertEqual('Device', device[1].tag)
        self.assertEqual(4, len(device[0].items()))
        self.assertEqual('Channel', device[0].tag)
        self.assertEqual(('name', "ECU"), device[1].items()[2])
        self.assertEqual(2, len(device))

    def test_channel_tag(self):
        channel = self.header().Configuration().HardwareConfiguration().Device().get_Channels()[0]
        self.assertNotEqual([], channel)
        self.assertEqual('Channel', channel[1].tag)
        self.assertEqual(5, len(channel[0].items()))
        self.assertEqual('bit', channel[1].items()[2][0])

    def test_single_module_configuration(self):
        single_module_configuration = self.header().Configuration().ModuleConfiguration().get_SingleModuleConfiguration()
        self.assertIsNotNone(single_module_configuration)
        self.assertEqual('SingleModuleConfiguration', single_module_configuration.tag)
        self.assertEqual(('moduleName', './cameraModule'), single_module_configuration.items()[1])
        self.assertEqual(2, len(single_module_configuration.items()))
        self.assertEqual(3, len(list(single_module_configuration)))
        self.assertEqual('Argument', list(single_module_configuration)[1].tag)

    def test_module_configuration(self):
        module_configuration = self.header().Configuration().get_ModuleConfiguration()
        self.assertIsNotNone(module_configuration)
        self.assertEqual('ModuleConfiguration', module_configuration.tag)
        self.assertEqual('SingleModuleConfiguration', list(module_configuration)[0].tag)
        self.assertEqual(2, len(list(module_configuration)))

    def test_argument_tag(self):
        argument = self.header().Configuration().ModuleConfiguration().SingleModuleConfiguration().get_Argmuents()[1]
        self.assertNotEqual([], argument)
        self.assertEqual('Argument', argument[1].tag)
        self.assertEqual(2, len(argument[0].items()))
        self.assertEqual('flag', argument[1].items()[0][0])

    def test_stream_display_tag(self):
        stream_display = self.header().Configuration().get_StreamDisplay()
        self.assertIsNotNone(stream_display)
        self.assertEqual('StreamDisplay', stream_display.tag)
        self.assertEqual(3, len(stream_display.items()))
        self.assertEqual(('pages', '2'), stream_display.items()[2])

    def test_aux_display_configuration_tag(self):
        aux_display_configuration = self.header().Configuration().get_AuxDisplayConfiguration()
        self.assertIsNotNone(aux_display_configuration)
        self.assertEqual('AuxDisplayConfiguration', aux_display_configuration.tag)
        self.assertEqual('DispChannel', list(aux_display_configuration)[0].tag)
        self.assertEqual(2, len(list(aux_display_configuration)))

    def test_disp_channel_tag(self):
        disp_channel = self.header().Configuration().ModuleConfiguration().SingleModuleConfiguration().get_DispChannels()[1]
        self.assertNotEqual([], disp_channel)
        self.assertEqual('DispChannel', disp_channel[1].tag)
        self.assertEqual(5, len(disp_channel[0].items()))
        self.assertEqual('analyze', disp_channel[1].items()[0][0])

    def test_spike_configuration_tag(self):
        spike_configuration = self.header().Configuration().get_SpikeConfiguration()
        self.assertIsNotNone(spike_configuration)
        self.assertEqual('SpikeConfiguration', spike_configuration.tag)
        self.assertEqual('SpikeNTrode', list(spike_configuration)[1].tag)
        self.assertEqual(2, len(list(spike_configuration)))
        self.assertEqual(('categories', ''), spike_configuration.items()[0])

    def test_spike_n_trode_tag(self):
        spike_n_trode = self.header().Configuration().SpikeConfiguration().get_SpikeNTrode()
        self.assertIsNotNone(spike_n_trode)
        self.assertEqual('SpikeNTrode', spike_n_trode.tag)
        self.assertEqual('SpikeChannel', list(spike_n_trode)[1].tag)
        self.assertEqual(15, len(list(spike_n_trode)))
        self.assertEqual(('thresh'), spike_n_trode.items()[2][0])

    def test_spike_channel_tag(self):
        spike_channel = self.header().Configuration().SpikeConfiguration().SpikeNTrode().get_SpikeChannels()[0]
        self.assertIsNotNone(spike_channel)
        self.assertEqual('SpikeNTrode', spike_channel.tag)
        self.assertEqual(4, len(spike_channel.items()))
        self.assertEqual(('thresh'), spike_channel.items()[2][0])

