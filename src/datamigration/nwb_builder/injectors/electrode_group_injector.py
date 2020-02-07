class ElectrodeGroupInjector:

    def inject_all_electrode_groups(self, nwb_content, electrode_groups):
        for electrode_group in electrode_groups.values():
            self._inject_electrode_group(nwb_content, electrode_group)

    @staticmethod
    def _inject_electrode_group(nwb_content, electrode_group):
        nwb_content.add_electrode_group(electrode_group)
