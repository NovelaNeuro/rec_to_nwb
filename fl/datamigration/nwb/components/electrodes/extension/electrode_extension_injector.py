import logging.config
import os

from fl.datamigration.exceptions.not_compatible_metadata import NotCompatibleMetadata

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodeExtensionInjector:

    def inject_extensions(self, nwb_content, fl_electrode_extension):
        self.__check_extension_length(
            fl_electrode_extension.rel_x,
            fl_electrode_extension.rel_y,
            fl_electrode_extension.rel_z,
            fl_electrode_extension.hw_chan,
            fl_electrode_extension.ntrode_id,
            fl_electrode_extension.bad_channels
        )

        self.__join_extensions_to_electrodes(nwb_content, fl_electrode_extension )

    @staticmethod
    def __check_extension_length(*args):
        if len(set(map(len, args))) != 1:
            message = 'Electrodes metadata are not compatible!'
            logger.error(message)
            raise NotCompatibleMetadata(message)

    @staticmethod
    def __adjust_extension_length(rel_x, extension, msg):
        diff_in_length = len(rel_x) - len(extension)

        if diff_in_length == 0:
            return extension
        if diff_in_length > 0:
            for _ in range(diff_in_length):
                extension.append(0.0)

            message = 'Metadata are not compatible for electrodes! ' + str(
                diff_in_length) + ' elements in ' + msg + ' were populated by "0.0" '
            logger.exception(message)

            return extension

        message = 'Metadata are not compatible for electrodes! ' + str(
            diff_in_length * (-1)) + ' elements in ' + msg + ' were cutted off '
        logger.exception(message)

        return extension[:diff_in_length]

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
