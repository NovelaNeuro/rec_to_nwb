from fldatamigration.processing.nwb.components.device.fl_header_device import FlHeaderDevice


class FlHeaderDeviceBuilder:

    @staticmethod
    def build(name, global_configuration):
        return FlHeaderDevice(name, global_configuration)