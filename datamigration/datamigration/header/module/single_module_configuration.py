from .argument import Argument


class SingleModuleConfiguration:

    def __init__(self, element):
        self.tree = element
        self.arguments = \
            [Argument(argument_element) for argument_element in self.tree.findall('Argument')]
        self.tag = self.tree.tag
        self.send_trodes_config = self.tree.get('sendTrodesConfig')
        self.module_name = self.tree.get('moduleName')
        self.send_network_info = self.tree.get('sendNetworkInfo')
