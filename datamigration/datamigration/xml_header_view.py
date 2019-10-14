import xml.etree.ElementTree as ET


class Header:

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.file_name = filename

    def get_configuration(self):
        return self.tree.getroot()

    class Configuration:

        def __init__(self):
            header_instance = Header()
            self.tree = header_instance.tree

        def get_global_configuration(self):
            return self.tree.getroot().find('GlobalConfiguration')

        def get_hardware_configuration(self):
            return self.tree.getroot().find('HardwareConfiguration')

        def get_module_configuration(self):
            return self.tree.getroot().find('ModuleConfiguration')

        def get_stream_display(self):
            return self.tree.getroot().find('StreamDisplay')

        def get_aux_display_configuration(self):
            return self.tree.getroot().find('AuxDisplayConfiguration')

        def get_spike_configuration(self):
            return self.tree.getroot().find('SpikeConfiguration')

        class GlobalConfiguration:

            pass

        class HardwareConfiguration:

            def __init__(self):
                configuration = Header.Configuration()
                self.tree = configuration.tree

            def get_devices(self):
                return self.tree.getroot().find('HardwareConfiguration').findall('Device')

            class Device:

                def __init__(self):
                    hardware_configuration = Header.Configuration.HardwareConfiguration()
                    self.tree = hardware_configuration.tree

                def get_channels(self):
                    return self.tree.getroot().find('HardwareConfiguration').find('Device').findall('Channel')

        class ModuleConfiguration:

            def __init__(self):
                configuration = Header.Configuration()
                self.tree = configuration.tree

            def get_single_module_configurations(self):
                return self.tree.getroot().find('ModuleConfiguration').findall('SingleModuleConfiguration')

            class SingleModuleConfiguration:

                def __init__(self):
                    module_configuration = Header.Configuration.ModuleConfiguration()
                    self.tree = module_configuration.tree

                def get_arguments(self):
                    return self.tree.getroot().find('ModuleConfiguration').find('SingleModuleConfiguration').findall('Argument')

        class StreamDisplay:

            pass

        class AuxDisplayConfiguration:

            def __init__(self):
                configuration = Header.Configuration()
                self.tree = configuration.tree

            def get_disp_channels(self):
                return self.tree.getroot().find('AuxDisplayConfiguration').findall('DispChannel')

        class SpikeConfiguration:

            def __init__(self):
                configuration = Header.Configuration()
                self.tree = configuration.tree

            def get_spike_n_trodes(self):
                return self.tree.getroot().find('SpikeConfiguration').findall('SpikeNTrode')

            class SpikeNTrode:

                def __init__(self):
                    spike_configuration = Header.Configuration.SpikeConfiguration()
                    self.tree = spike_configuration.tree

                def get_spike_channels(self):
                    return self.tree.getroot().find('SpikeConfiguration').find('SpikeNTrode').findall('SpikeChannel')


