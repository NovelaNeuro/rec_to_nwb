import logging.config
import os

from rec_to_nwb.processing.nwb.components.device.fl_probe_manager import FlProbeManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ProbeOriginator:
    def __init__(self, device_factory, device_injector, probes_metadata):
        self.device_factory = device_factory
        self.device_injector = device_injector

        self.fl_probe_manager = FlProbeManager(probes_metadata)

    def make(self, nwb_content, shanks_dict, probes_valid_map, ):
        logger.info('Probes: Building')
        fl_probes = self.fl_probe_manager.get_fl_probes(shanks_dict, probes_valid_map)
        logger.info('Probes: Creating probes')
        probes = [self.device_factory.create_probe(fl_probe) for fl_probe in fl_probes]
        logger.info('Probes: Injecting probes into NWB')
        self.device_injector.inject_all_devices(nwb_content, probes)
        return probes
