from src.datamigration.tools.validate_input_parameters import validate_input_parameters


class ElectrodeGroupInjector:

    def inject_all_electrode_groups(self, nwb_content, electrode_groups):
        """insert electrode groups to nwb file"""

        validate_input_parameters(__name__, nwb_content, electrode_groups)
        for electrode_group in electrode_groups:
            self.__inject_electrode_group(nwb_content, electrode_group)

    @staticmethod
    def __inject_electrode_group(nwb_content, electrode_group):
        nwb_content.add_electrode_group(electrode_group)
