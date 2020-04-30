import copy
import logging.config
import os

from fl.datamigration.exceptions.not_compatible_metadata import NotCompatibleMetadata
from fl.datamigration.header.module.header import Header
from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension import FlElectrodeExtension
from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension_builder import \
    FlElectrodeExtensionBuilder
from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension_factory import \
    FlElectrodeExtensionFactory
from fl.datamigration.tools.beartype.beartype import beartype

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class FlElectrodeExtensionManager:

    @beartype
    def __init__(self, probes_metadata: list, metadata: dict, header: Header):
        self.probes_metadata = probes_metadata
        self.metadata = metadata
        self.header = header

    @beartype
    def get_fl_electrodes_extension(self, electrodes_valid_map: list) -> FlElectrodeExtension:
        probes_metadata = self.probes_metadata
        electrode_groups_metadata = self.metadata['electrode groups']
        ntrode_metadata = self.metadata['ntrode electrode group channel map']
        spike_n_trodes = self.header.configuration.spike_configuration.spike_n_trodes

        rel = FlElectrodeExtensionFactory.create_rel(
            probes_metadata=probes_metadata,
            electrode_groups_metadata=electrode_groups_metadata
        )
        hw_chan = FlElectrodeExtensionFactory.create_hw_chan(
            spike_n_trodes=spike_n_trodes
        )
        ntrode_id = FlElectrodeExtensionFactory.create_ntrode_id(
            ntrode_metadata=ntrode_metadata
        )
        bad_channels = FlElectrodeExtensionFactory.create_bad_channels(
            ntrode_metadata=ntrode_metadata
        )
        probe_shank = FlElectrodeExtensionFactory.create_probe_shank(
            probes_metadata=probes_metadata,
            electrode_groups_metadata=electrode_groups_metadata
        )
        probe_channel = FlElectrodeExtensionFactory.create_probe_channel(
            ntrode_metadata=ntrode_metadata
        )

        self.__validate_extension_length(
            electrodes_valid_map,
            rel['rel_x'],
            rel['rel_y'],
            rel['rel_z'],
            hw_chan,
            ntrode_id,
            bad_channels,
            probe_shank,
            probe_channel
        )

        return FlElectrodeExtensionBuilder.build(
            rel_x=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, rel['rel_x']),
            rel_y=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, rel['rel_y']),
            rel_z=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, rel['rel_z']),
            hw_chan=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, hw_chan),
            ntrode_id=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, ntrode_id),
            bad_channels=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, bad_channels),
            probe_shank=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, probe_shank),
            probe_channel=self.__filter_extension_list_with_electrodes_valid_map(electrodes_valid_map, probe_channel),
        )

    @staticmethod
    def __validate_extension_length(*args):
        if len(set(map(len, args))) != 1:
            message = 'Electrodes metadata are not compatible!'
            logger.error(message)
            raise NotCompatibleMetadata(message)

    @staticmethod
    @beartype
    def __filter_extension_list_with_electrodes_valid_map(electrodes_valid_map: list, extension: list):
        tmp_electrodes_valid_map = copy.deepcopy(electrodes_valid_map)
        return [value for value in extension if tmp_electrodes_valid_map.pop(0)]
