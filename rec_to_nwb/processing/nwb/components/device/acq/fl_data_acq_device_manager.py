from rec_to_nwb.processing.nwb.components.device.acq.fl_data_acq_device_builder import FlDataAcqDeviceBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlDataAcqDeviceManager:

    @beartype
    def __init__(self, metadata: list):
        self.metadata = metadata

    def get_fl_data_acq_device(self):
        return [
            self.__build_single_data_acq_device(acq_device_metadata)
            for acq_device_metadata in self.metadata
        ]

    @staticmethod
    @beartype
    def __build_single_data_acq_device(acq_device_metadata: dict):
        return FlDataAcqDeviceBuilder.build(
            name=acq_device_metadata['name'],
            system=acq_device_metadata['system'],
            amplifier=acq_device_metadata.get('amplifier', ''),
            adc_circuit=acq_device_metadata.get('adc_circuit', '')
        )
