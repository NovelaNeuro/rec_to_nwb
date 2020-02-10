import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodeExtensionInjector:

    def inject_extensions(self, nwb_content, electrodes_metadata_extension, hw_chan):

        hw_chan = self.__validate_and_adjust_hw_chan_length(electrodes_metadata_extension.rel_x, hw_chan)

        self.__join_extensions_to_electrodes(electrodes_metadata_extension, hw_chan, nwb_content)

    @staticmethod
    def __join_extensions_to_electrodes(electrodes_metadata_extension, hw_chan, nwb_content):
        nwb_content.electrodes.add_column(
            name='hwChan',
            description='None',
            data=hw_chan
        )
        nwb_content.electrodes.add_column(
            name='rel_x',
            description='None',
            data=electrodes_metadata_extension.rel_x
        )
        nwb_content.electrodes.add_column(
            name='rel_y',
            description='None',
            data=electrodes_metadata_extension.rel_y
        )
        nwb_content.electrodes.add_column(
            name='rel_z',
            description='None',
            data=electrodes_metadata_extension.rel_z
        )

    @staticmethod
    def __validate_and_adjust_hw_chan_length(rel_x, hw_chan):
        diff_in_length = len(rel_x) - len(hw_chan)

        if diff_in_length == 0:
            return hw_chan
        elif diff_in_length > 0:
            for _ in range(diff_in_length):
                hw_chan.append(0.0)

            message = 'Metadata and header are not compatible for electrodes! ' + str(
                diff_in_length) + ' elements in hw_chan_extension were populated by "0.0" '
            logger.exception(message)

            return hw_chan
        elif diff_in_length < 0:
            message = 'Metadata and header are not compatible for electrodes! ' + str(
                diff_in_length*(-1)) + ' elements in hw_chan_extension were cutted off '
            logger.exception(message)

            return hw_chan[:diff_in_length]
        else:
            return None
