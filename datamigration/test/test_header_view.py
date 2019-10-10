import unittest

from datamigration.datamigration import xml_header_view


class TestHeaderInterface(unittest.TestCase):

    def setUp(self):
        self.header = xml_header_view.XmlHeaderView(filename='fl_lab_sample_header.xml')

    def test_configuration_tag(self):
        configuration = self.header.get_Configuration()
        self.assertIsNotNone(configuration)
        self.assertEqual('Configuration', configuration.tag)
        self.assertEqual([], configuration.items())
        self.assertEqual(6, len(list(configuration)))

    def test_global_configuration_tag(self):
        global_configuration = self.header.get_GlobalConfiguration()
        self.assertIsNotNone(global_configuration)
        self.assertEqual('GlobalConfiguration', global_configuration.tag)
        self.assertEqual(('compileDate', 'May 16 2019'), global_configuration.items()[10])
        self.assertEqual(20, len(global_configuration.items()))
        self.assertEqual(0, len(list(global_configuration)))

    def test_hardware_configuration_tag(self):
        hardware_configuration = self.header.get_HardwareConfiguration()
        self.assertIsNotNone(hardware_configuration)
        self.assertEqual('HardwareConfiguration', hardware_configuration.tag)
        self.assertEqual(('samplingRate', '30000'), hardware_configuration.items()[0])
        self.assertEqual(2, len(hardware_configuration.items()))
        self.assertEqual(2, len(list(hardware_configuration)))
        self.assertEqual('Device', list(hardware_configuration)[1].tag)

    def test_device_tag(self):
        devices = self.header.get_Devices()
        self.assertNotEqual([], devices)
        for each_device in devices:
            self.assertEqual('Device', each_device.tag)
            self.assertEqual(4, len(each_device.items()))
            self.assertEqual('Channel', list(each_device)[1].tag)
        self.assertEqual(('name', "ECU"), devices[1].items()[2])
        self.assertEqual(2, len(devices))

    def test_channel_tag(self):
        channels = self.header.get_Channels()
        self.assertNotEqual([], channels)
        for each_channel in channels:
            self.assertEqual('Channel', each_channel.tag)
            self.assertEqual(5, len(each_channel.items()))
            self.assertEqual('bit', each_channel.items()[2][0])
