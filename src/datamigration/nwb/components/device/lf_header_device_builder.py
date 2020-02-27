from src.datamigration.nwb.components.device.lf_header_device import LfHeaderDevice


class LfHeaderDeviceBuilder:

    @staticmethod
    def build(name, global_configuration):
        return LfHeaderDevice(name, global_configuration)