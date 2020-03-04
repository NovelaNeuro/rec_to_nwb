from lf.datamigration.tools.validate_input_parameters import validate_input_parameters


class DeviceInjector:

    def inject_all_devices(self, nwb_content, devices):
        validate_input_parameters(__name__, nwb_content, devices)
        for device in devices:
            self.__inject_device(nwb_content, device)

    @staticmethod
    def __inject_device(nwb_content, device):
        nwb_content.add_device(device)