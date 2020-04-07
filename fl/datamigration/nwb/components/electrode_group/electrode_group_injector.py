from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class ElectrodeGroupInjector:

    def inject_all_electrode_groups(self, nwb_content, electrode_groups):
        """insert electrode groups to nwb file"""
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(electrode_groups))
        validation_registrator.validate()

        for electrode_group in electrode_groups:
            single_group_validation_registrator = ValidationRegistrator()
            single_group_validation_registrator.register(NotNoneValidator(nwb_content))
            single_group_validation_registrator.register(NotNoneValidator(electrode_group))
            single_group_validation_registrator.validate()

            self.__inject_electrode_group(nwb_content, electrode_group)

    @staticmethod
    def __inject_electrode_group(nwb_content, electrode_group):
        nwb_content.add_electrode_group(electrode_group)
