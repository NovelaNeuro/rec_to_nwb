from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class ElectrodeGroupInjector:

    def inject_all_electrode_groups(self, nwb_content, electrode_groups):
        """insert electrode groups to nwb file"""

        validate_parameters_not_none(__name__, nwb_content, electrode_groups)
        for electrode_group in electrode_groups:
            self.__inject_electrode_group(nwb_content, electrode_group)

    @staticmethod
    def __inject_electrode_group(nwb_content, electrode_group):
        nwb_content.add_electrode_group(electrode_group)
