from rec_to_nwb.processing.nwb.components.device.header.fl_header_device import \
    FlHeaderDevice


class FlHeaderDeviceBuilder:

    @staticmethod
    def build(name, global_configuration):
        return FlHeaderDevice(name, global_configuration)
