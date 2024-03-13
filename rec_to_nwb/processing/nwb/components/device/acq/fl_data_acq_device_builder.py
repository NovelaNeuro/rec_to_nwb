from rec_to_nwb.processing.nwb.components.device.acq.fl_data_acq_device import \
    FlDataAcqDevice
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlDataAcqDeviceBuilder:

    @staticmethod
    @beartype
    def build(name, system, amplifier, adc_circuit):
        return FlDataAcqDevice(
            name=name,
            system=system,
            amplifier=amplifier,
            adc_circuit=adc_circuit
        )
