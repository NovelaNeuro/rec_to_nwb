from fl.datamigration.tools.name_extractor import NameExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class DeviceInjector:

    def inject_all_devices(self, nwb_content, devices):
        validate_parameters_not_none(
            class_name=__name__,
            args=[nwb_content, devices],
            args_name=[NameExtractor.extract_name(self.inject_all_devices)[1],
                       NameExtractor.extract_name(self.inject_all_devices)[2]]
        )

        for device in devices:
            self.__inject_device(nwb_content, device)

    @staticmethod
    def __inject_device(nwb_content, device):
        nwb_content.add_device(device)