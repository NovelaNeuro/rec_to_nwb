import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodeExtensionInjector:

    def inject_extensions(self, nwb_content, metadata_extension, header_extension, ntrodes_extension):

        header_extension = self.__adjust_extension_length(
            metadata_extension.rel_x,
            header_extension,
            'header_extension'
        )
        ntrodes_extension = self.__adjust_extension_length(
            metadata_extension.rel_x,
            ntrodes_extension,
            'ntrodes_extension'
        )

        self.__join_extensions_to_electrodes(metadata_extension, header_extension, ntrodes_extension, nwb_content)

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

        else:
            message = 'Metadata are not compatible for electrodes! ' + str(
                diff_in_length * (-1)) + ' elements in ' + msg + ' were cutted off '
            logger.exception(message)

            return extension[:diff_in_length]

    @staticmethod
    def __join_extensions_to_electrodes(metadata_extension, header_extension, ntrodes_extension, nwb_content):
        nwb_content.electrodes.add_column(
            name='hwChan',
            description='None',
            data=header_extension
        )
        nwb_content.electrodes.add_column(
            name='ntrode_id',
            description='None',
            data=ntrodes_extension
        )
        nwb_content.electrodes.add_column(
            name='rel_x',
            description='None',
            data=metadata_extension.rel_x
        )
        nwb_content.electrodes.add_column(
            name='rel_y',
            description='None',
            data=metadata_extension.rel_y
        )
        nwb_content.electrodes.add_column(
            name='rel_z',
            description='None',
            data=metadata_extension.rel_z
        )
