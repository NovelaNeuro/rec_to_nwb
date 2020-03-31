import logging.config
import os

import numpy as np
from fl.datamigration.validation.ntrode_validation_summary import NTrodeValidationSummary
from fl.datamigration.exceptions.invalid_header_exception import InvalidHeaderException
from fl.datamigration.exceptions.invalid_metadata_exception import InvalidMetadataException
from fl.datamigration.validation.validator import Validator

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NTrodeValidator(Validator):

    def __init__(self, metadata, header):
        self.metadata = metadata
        self.header = header

    def createSummary(self):
        ntrodes = self.metadata['ntrode probe channel map']
        if (len(ntrodes) == 0):
            raise InvalidMetadataException("There are no ntrodes defined in metadata.yml file.")
        if self.header is None or \
                self.header.configuration.spike_configuration is None or \
                self.header.configuration.spike_configuration.spike_n_trodes is None:
            raise InvalidHeaderException("Rec header does not contain spike_n_trodes data")

        spike_ntrodes = self.header.configuration.spike_configuration.spike_n_trodes
        ntrodes_num = len(ntrodes)
        spike_ntrodes_num = len(spike_ntrodes)
        return NTrodeValidationSummary(ntrodes_num, spike_ntrodes_num)
