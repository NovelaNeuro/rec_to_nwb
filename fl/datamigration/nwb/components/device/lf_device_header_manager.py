from fl.datamigration.nwb.components.device.fl_header_device_builder import LfHeaderDeviceBuilder


class LfDeviceHeaderManager:

    def __init__(self, name, global_configuration):
        self.name = name
        self.global_configuration = global_configuration

    def get_fl_header_device(self):
        return LfHeaderDeviceBuilder.build(self.name, self.global_configuration)