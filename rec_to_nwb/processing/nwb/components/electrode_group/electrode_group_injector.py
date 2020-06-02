from pynwb import NWBFile

from rec_to_nwb.processing.tools.beartype.beartype import beartype


class ElectrodeGroupInjector:

    @beartype
    def inject_all_electrode_groups(self, nwb_content: NWBFile, electrode_groups: list):
        """insert electrode groups to nwb file"""

        for electrode_group in electrode_groups:
            self.__inject_electrode_group(nwb_content, electrode_group)

    @staticmethod
    def __inject_electrode_group(nwb_content, electrode_group):
        nwb_content.add_electrode_group(electrode_group)
