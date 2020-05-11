import logging.config
import os

from pynwb import NWBFile

from rec_to_nwb.processing.nwb.components.electrodes.extension.fl_electrode_extension import FlElectrodeExtension
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodeExtensionInjector:

    @beartype
    def inject_extensions(self, nwb_content: NWBFile, fl_electrode_extension: FlElectrodeExtension):
        validate_parameters_not_none(
            __name__,
            fl_electrode_extension.rel_x,
            fl_electrode_extension.rel_y,
            fl_electrode_extension.rel_z,
            fl_electrode_extension.hw_chan,
            fl_electrode_extension.ntrode_id,
            fl_electrode_extension.channel_id,
            fl_electrode_extension.bad_channels,
            fl_electrode_extension.probe_shank,
            fl_electrode_extension.probe_channel
        )
        self.__join_extensions_to_electrodes(nwb_content, fl_electrode_extension)

    @staticmethod
    def __join_extensions_to_electrodes(nwb_content, fl_electrode_extension):
        nwb_content.electrodes.add_column(
            name='hwChan',
            description='None',
            data=fl_electrode_extension.hw_chan
        )
        nwb_content.electrodes.add_column(
            name='ntrode_id',
            description='None',
            data=fl_electrode_extension.ntrode_id
        )
        nwb_content.electrodes.add_column(
            name='channel_id',
            description='None',
            data=fl_electrode_extension.channel_id
        )
        nwb_content.electrodes.add_column(
            name='bad_channel',
            description='None',
            data=fl_electrode_extension.bad_channels
        )
        nwb_content.electrodes.add_column(
            name='rel_x',
            description='None',
            data=fl_electrode_extension.rel_x
        )
        nwb_content.electrodes.add_column(
            name='rel_y',
            description='None',
            data=fl_electrode_extension.rel_y
        )
        nwb_content.electrodes.add_column(
            name='rel_z',
            description='None',
            data=fl_electrode_extension.rel_z
        )
        nwb_content.electrodes.add_column(
            name='probe_shank',
            description='None',
            data=fl_electrode_extension.probe_shank
        )
        nwb_content.electrodes.add_column(
            name='probe_channel',
            description='None',
            data=fl_electrode_extension.probe_channel
        )
