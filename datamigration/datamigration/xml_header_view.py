import xml.etree.ElementTree as ET


tree = ET.parse('fl_lab_sample_header.xml')


class Header:

    def __init__(self):
        pass

    @staticmethod
    def get_configuration():
        return tree.getroot()

    class Configuration:

        @staticmethod
        def get_global_configuration():
            return tree.getroot().find('GlobalConfiguration')

        @staticmethod
        def get_hardware_configuration():
            return tree.getroot().find('HardwareConfiguration')

        @staticmethod
        def get_module_configuration():
            return tree.getroot().find('ModuleConfiguration')

        @staticmethod
        def get_stream_display():
            return tree.getroot().find('StreamDisplay')

        @staticmethod
        def get_aux_display_configuration():
            return tree.getroot().find('AuxDisplayConfiguration')

        @staticmethod
        def get_spike_configuration():
            return tree.getroot().find('SpikeConfiguration')

        class GlobalConfiguration:

            pass

        class HardwareConfiguration:

            @staticmethod
            def get_devices():
                return tree.getroot().find('HardwareConfiguration').findall('Device')

            class Device:

                @staticmethod
                def get_channels():
                    return tree.getroot().find('HardwareConfiguration').find('Device').findall('Channel')

        class ModuleConfiguration:

            @staticmethod
            def get_single_module_configurations():
                return tree.getroot().find('ModuleConfiguration').findall('SingleModuleConfiguration')

            class SingleModuleConfiguration:

                @staticmethod
                def get_arguments():
                    return tree.getroot().find('ModuleConfiguration').find('SingleModuleConfiguration').findall('Argument')

        class StreamDisplay:

            pass

        class AuxDisplayConfiguration:

            @staticmethod
            def get_disp_channels():
                return tree.getroot().find('AuxDisplayConfiguration').findall('DispChannel')

        class SpikeConfiguration:

            @staticmethod
            def get_spike_n_trodes():
                return tree.getroot().find('SpikeConfiguration').findall('SpikeNTrode')

            class SpikeNTrode:

                @staticmethod
                def get_spike_channels():
                    return tree.getroot().find('SpikeConfiguration').find('SpikeNTrode').findall('SpikeChannel')


