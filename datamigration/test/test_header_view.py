import unittest
from datamigration.datamigration.header.module import header


class TestHeaderInterface(unittest.TestCase):

    def setUp(self):
        self.header = header.Header('fl_lab_sample_header.xml')

    def test_configuration_tag(self):
        configuration = self.header.configuration
        self.assertIsNotNone(configuration)
        self.assertEqual('Configuration', configuration.tag)

    def test_module_configuration_tag(self):
        module_configuration = self.header.configuration.module_configuration
        self.assertIsNotNone(module_configuration)
        self.assertEqual('ModuleConfiguration', module_configuration.tag)
        self.assertEqual(2, len(module_configuration.single_module_configurations))

    def test_single_module_configuration_tag(self):
        single_module_configurations = self.header.configuration.module_configuration.single_module_configurations
        self.assertIsNotNone(single_module_configurations)
        self.assertEqual('SingleModuleConfiguration', single_module_configurations[1].tag)
        self.assertEqual('1', single_module_configurations[0].send_trodes_config)
        self.assertEqual('./stateScript', single_module_configurations[1].module_name)
        self.assertEqual('1', single_module_configurations[1].send_network_info)

    def test_argument_tag(self):
        arguments = self.header.configuration.module_configuration.single_module_configurations[1].arguments
        self.assertIsNotNone(arguments)
        self.assertEqual('Argument', arguments[1].tag)
        self.assertEqual('-suppressUpdates', arguments[0].flag)
        self.assertEqual('4', arguments[1].value)

    def test_global_configuration_tag(self):
        global_configuration = self.header.configuration.global_configuration
        self.assertIsNotNone(global_configuration)
        self.assertEqual('GlobalConfiguration', global_configuration.tag)
        self.assertEqual('00401 00003', global_configuration.headstage_serial)
        self.assertEqual('0', global_configuration.headstage_smart_ref_on)
        self.assertEqual('0', global_configuration.realtime_mode)
        self.assertEqual('0', global_configuration.headstage_auto_settle_on)
        self.assertEqual('38699433', global_configuration.timestamp_at_creation)
        self.assertEqual('2.2', global_configuration.controller_firmware_version)
        self.assertEqual('65535 65535', global_configuration.controller_serial)
        self.assertEqual('1', global_configuration.save_displayed_chan_only)
        self.assertEqual('3.9', global_configuration.headstage_firmware_version)
        self.assertEqual('5.9.8', global_configuration.qt_version)
        self.assertEqual('May 16 2019', global_configuration.compile_date)
        self.assertEqual('10:32:19', global_configuration.compile_time)
        self.assertEqual('myAnimal', global_configuration.file_prefix)
        self.assertEqual('0', global_configuration.headstage_gyro_sensor_on)
        self.assertEqual('0', global_configuration.headstage_mag_sensor_on)
        self.assertEqual('1.8.2', global_configuration.trodes_version)
        self.assertEqual('0', global_configuration.headstage_accel_sensor_on)
        self.assertEqual('heads/Release_1.8.2-0-g9a3e37c', global_configuration.commit_head)
        self.assertEqual('', global_configuration.file_path)
        self.assertEqual('1563323368633', global_configuration.system_time_at_creation)

    def test_hardware_configuration_tag(self):
        hardware_configuration = self.header.configuration.hardware_configuration
        self.assertIsNotNone(hardware_configuration)
        self.assertEqual('HardwareConfiguration', hardware_configuration.tag)
        self.assertEqual('30000', hardware_configuration.sampling_rate)
        self.assertEqual('128', hardware_configuration.num_channels)

    def test_device_tag(self):
        devices = self.header.configuration.hardware_configuration.devices
        self.assertIsNotNone(devices)
        self.assertEqual('Device', devices[0].tag)
        self.assertEqual('1', devices[0].num_bytes)
        self.assertEqual('1', devices[1].available)
        self.assertEqual('MCU_IO', devices[0].name)
        self.assertEqual('10', devices[0].packet_order_preference)

    def test_channel_tag(self):
        channels = self.header.configuration.hardware_configuration.devices[0].channels
        self.assertIsNotNone(channels)
        self.assertEqual('Channel', channels[1].tag)
        self.assertEqual('MCU_Din1', channels[0].id)
        self.assertEqual('0', channels[0].bit)
        self.assertEqual('0', channels[0].start_byte)
        self.assertEqual('1', channels[0].input)
        self.assertEqual('digital', channels[0].data_type)

    def test_stream_display_tag(self):
        stream_display = self.header.configuration.stream_display
        self.assertIsNotNone(stream_display)
        self.assertEqual('StreamDisplay', stream_display.tag)
        self.assertEqual('#030303', stream_display.background_color)
        self.assertEqual('2', stream_display.columns)
        self.assertEqual('2', stream_display.pages)

    def test_spike_configuration_tag(self):
        spike_configuration = self.header.configuration.spike_configuration
        self.assertIsNotNone(spike_configuration)
        self.assertEqual('SpikeConfiguration', spike_configuration.tag)
        self.assertEqual('', spike_configuration.categories)

    def test_aux_display_configuration_tag(self):
        aux_display_configuration = self.header.configuration.aux_display_configuration
        self.assertIsNotNone(aux_display_configuration)
        self.assertEqual('AuxDisplayConfiguration', aux_display_configuration.tag)

    def test_disp_channel_tag(self):
        disp_channels = self.header.configuration.aux_display_configuration.disp_channels
        self.assertIsNotNone(disp_channels)
        self.assertEqual('DispChannel', disp_channels[1].tag)
        self.assertEqual('1', disp_channels[0].analyze)
        self.assertEqual('2', disp_channels[1].max_disp)
        self.assertEqual('#aaaaaa', disp_channels[1].color)
        self.assertEqual('Din2', disp_channels[1].id)
        self.assertEqual('ECU', disp_channels[0].device)

    def test_spike_n_trode_tag(self):
        spike_n_trode = self.header.configuration.spike_configuration.spike_n_trodes
        self.assertIsNotNone(spike_n_trode)
        self.assertEqual('SpikeNTrode', spike_n_trode[0].tag)
        self.assertEqual('600', spike_n_trode[1].low_filter)
        self.assertEqual('1', spike_n_trode[1].lfp_chan)
        self.assertEqual('1', spike_n_trode[1].lfp_filter_on)
        self.assertEqual('0', spike_n_trode[1].ref_group)
        self.assertEqual('0', spike_n_trode[1].group_ref_on)
        self.assertEqual('400', spike_n_trode[1].lfp_high_filter)
        self.assertEqual('6000', spike_n_trode[1].hight_filter)
        self.assertEqual('#fce94f', spike_n_trode[1].color)
        self.assertEqual('1', spike_n_trode[1].ref_chan)
        self.assertEqual('2', spike_n_trode[1].id)
        self.assertEqual('0', spike_n_trode[1].lfp_ref_on)
        self.assertEqual('1', spike_n_trode[1].filter_on)
        self.assertEqual('0', spike_n_trode[1].ref_on)
        self.assertEqual('1', spike_n_trode[1].module_data_on)
        self.assertEqual('10', spike_n_trode[1].ref_n_trode_id)


    def test_spike_channel_tag(self):
        spike_channels = \
            self.header.configuration.spike_configuration.spike_n_trodes[1].spike_channels
        self.assertIsNotNone(spike_channels)
        self.assertEqual('SpikeChannel', spike_channels[0].tag)
        self.assertEqual('56', spike_channels[0].hw_chan)
        self.assertEqual('225', spike_channels[0].max_disp)
        self.assertEqual('60', spike_channels[0].thresh)
        self.assertEqual('1', spike_channels[0].trigger_on)









