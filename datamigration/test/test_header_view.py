import unittest
from datamigration.datamigration import xml_header_view


class TestHeaderInterface(unittest.TestCase):

    def setUp(self):
        self.header = xml_header_view.Header()

    def test_configuration_tag(self):
        configuration = self.header.get_configuration()
        self.assertIsNotNone(configuration)
        self.assertEqual('Configuration', configuration.tag)
        self.assertEqual([], configuration.items())
        self.assertEqual(6, len(list(configuration)))

    def test_global_configuration_tag(self):
        configuration_instance = self.header.Configuration()
        global_configuration = configuration_instance.get_global_configuration()
        self.assertIsNotNone(global_configuration)
        self.assertEqual('GlobalConfiguration', global_configuration.tag)
        self.assertEqual(('compileDate', 'May 16 2019'), global_configuration.items()[10])
        self.assertEqual(20, len(global_configuration.items()))
        self.assertEqual(0, len(list(global_configuration)))

    def test_hardware_configuration_tag(self):
        configuration_instance = self.header.Configuration()
        hardware_configuration = configuration_instance.get_hardware_configuration()
        self.assertIsNotNone(hardware_configuration)
        self.assertEqual('HardwareConfiguration', hardware_configuration.tag)
        self.assertEqual(('samplingRate', '30000'), hardware_configuration.items()[0])
        self.assertEqual(2, len(hardware_configuration.items()))
        self.assertEqual(2, len(list(hardware_configuration)))
        self.assertEqual('Device', list(hardware_configuration)[1].tag)

    def test_device_tag(self):
        hardware_configuration_instance = self.header.Configuration.HardwareConfiguration()
        device = hardware_configuration_instance.get_devices()[1]
        self.assertNotEqual([], device)
        self.assertEqual('Device', device.tag)
        self.assertEqual(4, len(device.items()))
        self.assertEqual('Channel', list(device)[0].tag)
        self.assertEqual(('name', "ECU"), device.items()[2])
        self.assertEqual(2, len(list(device)))

    def test_channel_tag(self):
        device_instance = self.header.Configuration.HardwareConfiguration.Device()
        channel = device_instance.get_channels()[0]
        self.assertNotEqual([], channel)
        self.assertEqual('Channel', channel.tag)
        self.assertEqual(5, len(channel.items()))
        self.assertEqual('bit', channel.items()[2][0])

    def test_single_module_configuration(self):
        module_configuration_instance = self.header.Configuration.ModuleConfiguration()
        single_module_configuration = module_configuration_instance.get_single_module_configurations()[0]
        self.assertIsNotNone(single_module_configuration)
        self.assertEqual('SingleModuleConfiguration', single_module_configuration.tag)
        self.assertEqual(('moduleName', './cameraModule'), single_module_configuration.items()[1])
        self.assertEqual(3, len(single_module_configuration.items()))
        self.assertEqual('Argument', list(single_module_configuration)[1].tag)

    def test_module_configuration(self):
        configuration_instance = self.header.Configuration()
        module_configuration = configuration_instance.get_module_configuration()
        self.assertIsNotNone(module_configuration)
        self.assertEqual('ModuleConfiguration', module_configuration.tag)
        self.assertEqual('SingleModuleConfiguration', list(module_configuration)[0].tag)
        self.assertEqual(2, len(list(module_configuration)))

    def test_argument_tag(self):
        single_module_configuration_instance = self.header.Configuration.ModuleConfiguration.SingleModuleConfiguration()
        argument = single_module_configuration_instance.get_arguments()[1]
        self.assertNotEqual([], argument)
        self.assertEqual('Argument', argument.tag)
        self.assertEqual(2, len(argument.items()))
        self.assertEqual('flag', argument.items()[0][0])

    def test_stream_display_tag(self):
        configuration_instance = self.header.Configuration()
        stream_display = configuration_instance.get_stream_display()
        self.assertIsNotNone(stream_display)
        self.assertEqual('StreamDisplay', stream_display.tag)
        self.assertEqual(3, len(stream_display.items()))
        self.assertEqual(('pages', '2'), stream_display.items()[2])

    def test_aux_display_configuration_tag(self):
        configuration_instance = self.header.Configuration()
        aux_display_configuration = configuration_instance.get_aux_display_configuration()
        self.assertIsNotNone(aux_display_configuration)
        self.assertEqual('AuxDisplayConfiguration', aux_display_configuration.tag)
        self.assertEqual('DispChannel', list(aux_display_configuration)[0].tag)
        self.assertEqual(2, len(list(aux_display_configuration)))

    def test_disp_channel_tag(self):
        aux_display_configuration_instance = self.header.Configuration.AuxDisplayConfiguration()
        disp_channel = aux_display_configuration_instance.get_disp_channels()[1]
        self.assertNotEqual([], disp_channel)
        self.assertEqual('DispChannel', disp_channel.tag)
        self.assertEqual(5, len(disp_channel.items()))
        self.assertEqual('analyze', disp_channel.items()[0][0])

    def test_spike_configuration_tag(self):
        configuration_instance = self.header.Configuration()
        spike_configuration = configuration_instance.get_spike_configuration()
        self.assertIsNotNone(spike_configuration)
        self.assertEqual('SpikeConfiguration', spike_configuration.tag)
        self.assertEqual('SpikeNTrode', list(spike_configuration)[1].tag)
        self.assertEqual(2, len(list(spike_configuration)))
        self.assertEqual(('categories', ''), spike_configuration.items()[0])

    def test_spike_n_trode_tag(self):
        spike_configuration_instance = self.header.Configuration.SpikeConfiguration()
        spike_n_trode = spike_configuration_instance.get_spike_n_trodes()[0]
        self.assertIsNotNone(spike_n_trode)
        self.assertEqual('SpikeNTrode', spike_n_trode.tag)
        self.assertEqual('SpikeChannel', list(spike_n_trode)[1].tag)
        self.assertEqual(15, len(spike_n_trode.items()))
        self.assertEqual('1', spike_n_trode.items()[2][1])

    def test_spike_channel_tag(self):
        spike_n_trode_instance = self.header.Configuration.SpikeConfiguration.SpikeNTrode()
        spike_channel = spike_n_trode_instance.get_spike_channels()[0]
        self.assertIsNotNone(spike_channel)
        self.assertEqual('SpikeChannel', spike_channel.tag)
        self.assertEqual(4, len(spike_channel.items()))
        self.assertEqual('thresh', spike_channel.items()[2][0])

