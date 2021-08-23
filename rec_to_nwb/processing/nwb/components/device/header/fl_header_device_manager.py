from rec_to_nwb.processing.nwb.components.device.header.fl_header_device_builder import \
    FlHeaderDeviceBuilder


class FlHeaderDeviceManager:

    def __init__(self, name, global_configuration, default_configuration):
        self.name = name
        self.global_configuration = global_configuration.__dict__
        self.default_configuration = default_configuration.__dict__

    def get_fl_header_device(self):
        return FlHeaderDeviceBuilder.build(self.name, self.__compare_global_configuration_with_default())

    def __compare_global_configuration_with_default(self):
        for single_key in self.default_configuration:
            if single_key not in self.global_configuration.keys() or self.global_configuration[single_key] is None:
                self.global_configuration[single_key] = self.default_configuration[single_key]
        return self.global_configuration
