import logging.config
import os

from src.datamigration.header.module.single_module_configuration import SingleModuleConfiguration

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ModuleConfiguration:

    def __init__(self, element):
        self.tree = element
        self.single_module_configurations = \
            [SingleModuleConfiguration(single_module_configuration_element)
             for single_module_configuration_element in self.tree.findall('SingleModuleConfiguration')]
        self.tag = self.tree.tag
