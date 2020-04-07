from fl.datamigration.nwb.components.electrodes.electrode_metadata_extension_creator import \
    ElectrodesMetadataExtensionCreator
from fl.datamigration.nwb.components.electrodes.electrode_ntrode_extension_creator import \
    ElectrodesNtrodeExtensionCreator
from fl.datamigration.nwb.components.electrodes.electrodes_header_extension_creator import \
    ElectrodesHeaderExtensionCreator
from fl.datamigration.tools.filter_probe_by_type import filter_probe_by_type
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class ElectrodeExtensionCreator:

    def __init__(self, probes_metadata, electrode_groups_metadata, ntrodes_metadata, header):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata
        self.ntrodes_metadata = ntrodes_metadata
        self.header = header

        self.electrodes_metadata_extension_creator = ElectrodesMetadataExtensionCreator()
        self.electrodes_header_extension_creator = ElectrodesHeaderExtensionCreator()
        self.electrodes_ntrodes_extension_creator = ElectrodesNtrodeExtensionCreator()

    def create(self):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.probes_metadata))
        validation_registrator.register(NotNoneValidator(self.electrode_groups_metadata))
        validation_registrator.register(NotNoneValidator(self.ntrodes_metadata))
        validation_registrator.register(NotNoneValidator(self.header))
        validation_registrator.validate()

        self._create_extension_from_metadata(self.electrode_groups_metadata, self.probes_metadata)

        electrodes_header_extension = self.electrodes_header_extension_creator.create_electrodes_header_extension(
            self.header.configuration.spike_configuration.spike_n_trodes
        )

        electrodes_metadata_extension = self.electrodes_metadata_extension_creator

        electrodes_ntrode_extension_ntrode_id = self.electrodes_ntrodes_extension_creator.\
            create_electrodes_ntrode_extension_ntrode_id(self.ntrodes_metadata)
        electrodes_ntrode_extension_bad_channels = self.electrodes_ntrodes_extension_creator.\
            create_electrodes_ntrode_extension_bad_channels(self.ntrodes_metadata)

        return electrodes_metadata_extension, electrodes_header_extension, electrodes_ntrode_extension_ntrode_id, \
               electrodes_ntrode_extension_bad_channels

    def _create_extension_from_metadata(self, electrode_groups_metadata, probes_metadata):
        for electrode_group_metadata in electrode_groups_metadata:
            probe_metadata = filter_probe_by_type(probes_metadata, electrode_group_metadata['device_type'])

            for shank in probe_metadata['shanks']:
                for electrode in shank['electrodes']:
                    self.electrodes_metadata_extension_creator.create_extensions(electrode)
