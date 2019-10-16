from .single_module_configuration import SingleModuleConfiguration


class ModuleConfiguration:

    def __init__(self, element):
        self.tree = element
        self.single_module_configurations = \
            [SingleModuleConfiguration(single_module_configuration_element)
             for single_module_configuration_element in self.tree.findall('SingleModuleConfiguration')]
        self.tag = self.tree.tag
