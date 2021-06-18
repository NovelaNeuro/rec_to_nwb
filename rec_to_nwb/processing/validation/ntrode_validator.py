import logging.config
import os

from rec_to_nwb.processing.exceptions.invalid_header_exception import InvalidHeaderException
from rec_to_nwb.processing.exceptions.invalid_metadata_exception import InvalidMetadataException
from rec_to_nwb.processing.header.module.header import Header
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.count_electrodes_in_ntrode import count_electrodes_in_ntrode
from rec_to_nwb.processing.tools.count_electrodes_in_probe import count_electrodes_in_probe
from rec_to_nwb.processing.tools.filter_probe_by_type import filter_probe_by_type
from rec_to_nwb.processing.validation.ntrode_validation_summary import NTrodeValidationSummary
from rec_to_nwb.processing.validation.validator import Validator

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NTrodeValidator(Validator):

    @beartype
    def __init__(self, metadata: dict, header: Header, probes_metadata: list):
        self.metadata = metadata
        self.header = header
        self.probes_metadata = probes_metadata

    def create_summary(self):
        ntrodes = self.metadata['ntrode electrode group channel map']
        if len(ntrodes) == 0:
            raise InvalidMetadataException("There are no ntrodes defined in metadata.yml file.")
        if self.header is None or \
                self.header.configuration.spike_configuration is None or \
                self.header.configuration.spike_configuration.spike_n_trodes is None:
            raise InvalidHeaderException("Rec header does not contain spike_n_trodes data")

        spike_ntrodes = self.header.configuration.spike_configuration.spike_n_trodes
        ntrodes_num = len(ntrodes)
        spike_ntrodes_num = len(spike_ntrodes)
        self.validate_ntrode_metadata_with_probe_metadata(self.metadata, self.probes_metadata)

        return NTrodeValidationSummary(ntrodes_num, spike_ntrodes_num)

    @staticmethod
    def validate_ntrode_metadata_with_probe_metadata(metadata, probes_metadata):
        for electrode_group in metadata['electrode_groups']:
            probe_metadata = filter_probe_by_type(probes_metadata, electrode_group['device_type'])
            electrodes_in_probe = count_electrodes_in_probe(probe_metadata)
            electrodes_in_group = count_electrodes_in_ntrode(
                metadata['ntrode electrode group channel map'],
                electrode_group['id']
            )
            if electrodes_in_probe != electrodes_in_group:
                raise InvalidMetadataException(
                    'Ntrode definition in metadata is not compatible with probe schema.' +
                    'Probe_type: ' + str(electrode_group['device_type']) +
                    ' electrodes in this probe_type: ' + str(electrodes_in_probe) +
                    '. Ntrode_metadata for electrode_group of id: ' + str(electrode_group['id']) +
                    ' electrodes in this electrode_group: ' + str(electrodes_in_group)
                )
