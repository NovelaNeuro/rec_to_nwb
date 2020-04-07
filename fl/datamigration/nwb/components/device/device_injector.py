from fl.datamigration.tools.validate_parameters import validate_parameters_not_none
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class DeviceInjector:

    def inject_all_devices(self, nwb_content, devices):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(nwb_content))
        validation_registrator.register(NotNoneValidator(devices))
        validation_registrator.validate()
        for device in devices:
            self.__inject_device(nwb_content, device)

    @staticmethod
    def __inject_device(nwb_content, device):
        nwb_content.add_device(device)