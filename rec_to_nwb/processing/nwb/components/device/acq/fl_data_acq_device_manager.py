from rec_to_nwb.processing.nwb.components.device.acq.fl_data_acq_device_builder import FlDataAcqDeviceBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlDataAcqDeviceManager:

    @beartype
    def __init__(self, metadata: list):
        self.metadata = metadata

    def get_fl_data_acq_device(self):
        return [
            self.__build_single_data_acq_device(acq_device_metadata, device_id)
            for device_id, acq_device_metadata in enumerate(self.metadata)
        ]

    @staticmethod
    @beartype
    def __build_single_data_acq_device(acq_device_metadata: dict, device_id: int):
        return FlDataAcqDeviceBuilder.build(
            name='dataacq_device' + str(device_id),
            system=acq_device_metadata['system'],
            amplifier=acq_device_metadata.get('amplifier', ''),
            adc_circuit=acq_device_metadata.get('adc_circuit', '')
        )
