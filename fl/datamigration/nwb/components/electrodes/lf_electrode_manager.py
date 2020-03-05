from fl.datamigration.nwb.components.electrodes.lf_electrode_builder import LfElectrodesBuilder
from fl.datamigration.tools.filter_probe_by_type import filter_probe_by_type
from fl.datamigration.tools.validate_input_parameters import validate_input_parameters


class LfElectrodeManager:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.lf_electrodes_builder = LfElectrodesBuilder()

    def get_lf_electrodes(self, electrode_groups):
        self.__validate_parameters(electrode_groups)
        lf_electrodes = []

        for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata):
            probe_metadata = filter_probe_by_type(self.probes_metadata, electrode_group_metadata['device_type'])

            for shank in probe_metadata['shanks']:
                for _ in shank['electrodes']:
                    lf_electrodes.append(self.lf_electrodes_builder.build(electrode_groups[counter]))

        return lf_electrodes

    def __validate_parameters(self, electrode_groups):
        validate_input_parameters(__name__, self.probes_metadata, self.electrode_groups_metadata, electrode_groups)
        [validate_input_parameters(__name__, electrode_group.name) for electrode_group in electrode_groups]






