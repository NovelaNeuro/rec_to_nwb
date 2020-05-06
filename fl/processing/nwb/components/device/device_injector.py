from fl.processing.tools.validate_parameters import validate_parameters_not_none


class DeviceInjector:

    def inject_all_devices(self, nwb_content, devices):
        validate_parameters_not_none(__name__, nwb_content, devices)
        for device in devices:
            self.__inject_device(nwb_content, device)

    @staticmethod
    def __inject_device(nwb_content, device):
        nwb_content.add_device(device)