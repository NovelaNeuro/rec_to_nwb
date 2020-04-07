from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class ElectrodesNtrodeExtensionCreator:

    @classmethod
    def create_electrodes_ntrode_extension_ntrode_id(cls, metadata):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(metadata))
        validation_registrator.validate()

        electrodes_ntrode_extension_ntrode_id = []
        for ntrode in metadata:
            electrodes_ntrode_extension_ntrode_id.extend([ntrode['ntrode_id']] * len(ntrode['map']))
        return electrodes_ntrode_extension_ntrode_id

    @classmethod
    def create_electrodes_ntrode_extension_bad_channels(cls, metadata):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(metadata))
        validation_registrator.validate()

        electrodes_ntrode_extension_bad_channels = []
        for ntrode in metadata:
            electrodes_ntrode_extension_bad_channels.extend([True if counter in ntrode['bad_channels'] else False
                                                             for counter, _ in enumerate(ntrode['map'])])
        return electrodes_ntrode_extension_bad_channels
