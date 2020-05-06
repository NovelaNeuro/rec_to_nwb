from fldatamigration.processing.nwb.components.device.fl_header_device_builder import FlHeaderDeviceBuilder


class FlDeviceHeaderManager:

    def __init__(self, name, global_configuration):
        self.name = name
        self.global_configuration = global_configuration

    def get_fl_header_device(self):
        return FlHeaderDeviceBuilder.build(self.name, self.global_configuration)