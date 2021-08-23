import logging.config
import os

from rec_to_nwb.processing.nwb.components.electrodes.extension.electrode_extension_injector import \
    ElectrodeExtensionInjector
from rec_to_nwb.processing.nwb.components.electrodes.extension.fl_electrode_extension_manager import \
    FlElectrodeExtensionManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodesExtensionOriginator:

    def __init__(self, probes, metadata, header):
        self.fl_electrode_extension_manager = FlElectrodeExtensionManager(
            probes,
            metadata,
            header
        )
        self.electrode_extension_injector = ElectrodeExtensionInjector()

    def make(self, nwb_content, electrodes_valid_map):
        logger.info('FlElectrodesExtensions: Building')
        fl_electrode_extension = self.fl_electrode_extension_manager.get_fl_electrodes_extension(
            electrodes_valid_map)
        logger.info('FlElectrodesExtensions: Injecting into NWB')
        self.electrode_extension_injector.inject_extensions(
            nwb_content,
            fl_electrode_extension
        )
