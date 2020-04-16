from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension_builder import \
    FlElectrodeExtensionBuilder


class FlElectrodeExtensionManager:

    def __init__(self, probes_metadata, metadata, header):
        self.probes_metadata = probes_metadata
        self.metadata = metadata
        self.header = header

    def get_fl_electrodes_extension(self):
        fl_electrode_extension_builder = FlElectrodeExtensionBuilder(
            probes_metadata=self.probes_metadata,
            electrode_groups_metadata=self.metadata['electrode groups'],
            ntrode_metadata=self.metadata['ntrode probe channel map'],
            header=self.header
        )
        return fl_electrode_extension_builder.build()
