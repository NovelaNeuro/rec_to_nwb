from unittest import TestCase

from rec_to_nwb.processing.nwb.components.device.acq.fl_data_acq_device import FlDataAcqDevice
from rec_to_nwb.processing.nwb.components.device.acq.fl_data_acq_device_manager import FlDataAcqDeviceManager


class TestFlDataAcqDeviceManager(TestCase):

    def test_fl_data_acq_device_manager_create_successfully_without_optional_data(self):
        metadata = [
            {'name': 'acq_0', 'system': 'system_0', 'amplifier': 'amplifier_0', 'adc_circuit': 'adc_circuit_0'},
            {'name': 'acq_1', 'system': 'system_1', 'amplifier': 'amplifier_1', 'adc_circuit': 'adc_circuit_1'}
        ]

        fl_data_acq_device_manager = FlDataAcqDeviceManager(metadata)
        fl_data_acq_device = fl_data_acq_device_manager.get_fl_data_acq_device()

        self.assertIsInstance(fl_data_acq_device[0], FlDataAcqDevice)

        self.assertIsInstance(fl_data_acq_device[0].system, str)
        self.assertIsInstance(fl_data_acq_device[0].amplifier, str)
        self.assertIsInstance(fl_data_acq_device[0].adc_circuit, str)

        self.assertEqual(fl_data_acq_device[0].name, 'acq_0')
        self.assertEqual(fl_data_acq_device[0].system, 'system_0')
        self.assertEqual(fl_data_acq_device[0].amplifier, 'amplifier_0')
        self.assertEqual(fl_data_acq_device[0].adc_circuit, 'adc_circuit_0')
        self.assertEqual(fl_data_acq_device[1].name, 'acq_1')
        self.assertEqual(fl_data_acq_device[1].system, 'system_1')
        self.assertEqual(fl_data_acq_device[1].amplifier, 'amplifier_1')
        self.assertEqual(fl_data_acq_device[1].adc_circuit, 'adc_circuit_1')

    def test_fl_data_acq_device_manager_create_successfully_with_optional_data(self):
        metadata = [
            {'name': 'acq_0', 'system': 'system_0', 'amplifier': 'amplifier_0', 'adc_circuit': 'adc_circuit_0'},
            {'name': 'acq_1', 'system': 'system_1'}
        ]

        fl_data_acq_device_manager = FlDataAcqDeviceManager(metadata)
        fl_data_acq_device = fl_data_acq_device_manager.get_fl_data_acq_device()

        self.assertIsInstance(fl_data_acq_device[0], FlDataAcqDevice)

        self.assertIsInstance(fl_data_acq_device[0].system, str)
        self.assertIsInstance(fl_data_acq_device[0].amplifier, str)
        self.assertIsInstance(fl_data_acq_device[0].adc_circuit, str)

        self.assertEqual(fl_data_acq_device[0].name, 'acq_0')
        self.assertEqual(fl_data_acq_device[0].system, 'system_0')
        self.assertEqual(fl_data_acq_device[0].amplifier, 'amplifier_0')
        self.assertEqual(fl_data_acq_device[0].adc_circuit, 'adc_circuit_0')
        self.assertEqual(fl_data_acq_device[1].name, 'acq_1')
        self.assertEqual(fl_data_acq_device[1].system, 'system_1')
        self.assertEqual(fl_data_acq_device[1].amplifier, '')
        self.assertEqual(fl_data_acq_device[1].adc_circuit, '')