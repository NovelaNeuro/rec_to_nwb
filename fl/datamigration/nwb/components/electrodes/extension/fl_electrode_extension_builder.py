from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension import FlElectrodeExtension
from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension_factory import \
    FlElectrodeExtensionFactory
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeExtensionBuilder:
    def __init__(self, probes_metadata, electrode_groups_metadata, ntrode_metadata, header):
        self.__validate_parameters(__name__, probes_metadata, electrode_groups_metadata, ntrode_metadata, header)

        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata
        self.ntrode_metadata = ntrode_metadata
        self.header = header

    def build(self):

        rel = FlElectrodeExtensionFactory.create_rel(
            probes_metadata=self.probes_metadata,
            electrode_groups_metadata=self.electrode_groups_metadata
        )

        hw_chan = FlElectrodeExtensionFactory.create_hw_chan(
            spike_n_trodes=self.header.configuration.spike_configuration.spike_n_trodes
        )

        ntrode_id = FlElectrodeExtensionFactory.create_ntrode_id(
            ntrode_metadata=self.ntrode_metadata
        )

        bad_channels = FlElectrodeExtensionFactory.create_bad_channels(
            ntrode_metadata=self.ntrode_metadata
        )
        probe_shank = FlElectrodeExtensionFactory.create_probe_shank(
            probes_metadata=self.probes_metadata,
            electrode_groups_metadata=self.electrode_groups_metadata
        )

        return FlElectrodeExtension(
            rel=rel,
            hw_chan=hw_chan,
            ntrode_id=ntrode_id,
            bad_channels=bad_channels,
            probe_shank=probe_shank
        )

    @staticmethod
    def __validate_parameters(class_name, probes_metadata, electrode_groups_metadata, ntrode_metadata, header):
        validate_parameters_not_none(class_name, probes_metadata, electrode_groups_metadata, ntrode_metadata, header)
