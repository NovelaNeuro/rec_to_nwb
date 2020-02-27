class ElectrodeGroupInjector:

    def inject_all_electrode_groups(self, nwb_content, electrode_groups):
        """insert electrode groups to nwb file"""

        for electrode_group in electrode_groups.values():
            self.__inject_electrode_group(nwb_content, electrode_group)

    @staticmethod
    def __inject_electrode_group(nwb_content, electrode_group):
        nwb_content.add_electrode_group(electrode_group)
