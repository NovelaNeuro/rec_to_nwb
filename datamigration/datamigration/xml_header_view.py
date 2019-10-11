import xml.etree.ElementTree as ET


class Header:

    def __init__(self, filename):
        global tree
        tree = ET.parse(filename)

    def get_Configuration(self):
        return self.tree.getroot()

    class Configuration:


        def get_GlobalConfiguration(self):
            return self.tree.getroot().find('GlobalConfiguration')

        def get_HardwareConfiguration(self):
            return self.tree.getroot().find('HardwareConfiguration')

        def get_ModuleConfiguration(self):
            return self.tree.getroot().find('ModuleConfiguration')

        def get_StreamDisplay(self):
            return self.tree.getroot().find('StreamDisplay')

        def get_AuxDisplayConfiguration(self):
            return self.tree.getroot().find('AuxDisplayConfiguration')

        def get_SpikeConfiguration(self):
            return self.tree.getroot().find('SpikeConfiguration')


        class GlobalConfiguration:

            pass


        class HardwareConfiguration:


            def get_Devices(self):
                return self.tree.getroot().find('HardwareConfiguration').findall('Device')


            class Device:


                def get_Channels(self):
                    return self.tree.getroot().find('HardwareConfiguration').find('Device').findall('Channel')

        class ModuleConfiguration:


            def get_SingleModuleConfiguration(self):
                return self.tree.getroot().find('ModuleConfiguration').findall('SingleModuleConfiguration')


            class SingleModuleConfiguration:


                def get_Arguments(self):
                    return self.tree.getroot().find('ModuleConfiguration').find('SingleModuleConfiguration').findall('Arguemnts')

        class StreamDisplay:

            pass


        class AuxDisplayConfiguration:


            def get_DispChannels(self):
                return self.tree.getroot().find('AuxDisplayConfiguration').findall('DispChannel')


        class SpikeConfiguration:


            def get_SpikeNTrodes(self):
                return self.tree.getroot().find('SpikeConfiguration').findall('SpikeNTrode')


            class SpikeNTrdoe:


                def get_SpikeChannels(self):
                    return self.tree.getroot().find('SpikeConfiguration').find('SpikeNTrode').findall('SpikeChannels')


