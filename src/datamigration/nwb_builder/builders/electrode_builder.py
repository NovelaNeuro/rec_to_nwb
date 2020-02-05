from src.datamigration.nwb_builder.creators.electrode_creator import ElectrodesCreator
from src.datamigration.tools.filter_probe_by_type import filter_probe_by_type


class ElectrodeBuilder:
    def __init__(self, probes_metadata, electrode_groups_metadata):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.electrodes_creator = ElectrodesCreator()

    def build(self, nwb_content, electrode_group_dict,):
        for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata):
            probe_metadata = filter_probe_by_type(self.probes_metadata, electrode_group_metadata['device_type'])
            for shank in probe_metadata['shanks']:
                for _ in shank['electrodes']:
                    self.electrodes_creator.create_electrode(nwb_content, electrode_group_dict[counter])






