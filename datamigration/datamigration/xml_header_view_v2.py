import xml.etree.ElementTree as ET


class Header:

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.configuration = Configuration(self.tree.getroot())


class Configuration:

    def __init__(self, element):
        self.tree = element
        self.module_configuration = ModuleConfiguration(self.tree.find('ModuleConfiguration'))
        self.global_configuration = GlobalConfiguration(self.tree.find('GlobalConfiguration'))
        self.spike_configuration = SpikeConfiguration(self.tree.find('SpikeConfiguration'))
        self.stream_display = StreamDisplay(self.tree.find('StreamDisplay'))
        self.hardware_configuration = HardwareConfiguration(self.tree.find('HardwareConfiguration'))
        self.aux_display_configuration = AuxDisplayConfiguration(self.tree.find('AuxDisplayConfiguration'))
        self.tag = self.tree.tag


class ModuleConfiguration:

    def __init__(self, element):
        self.tree = element
        self.single_module_configurations = \
            [SingleModuleConfiguration(single_module_configuration_element)
             for single_module_configuration_element in self.tree.findall('SingleModuleConfiguration')]
        self.tag = self.tree.tag


class SingleModuleConfiguration:

    def __init__(self, element):
        self.tree = element
        self.arguments = \
            [Argument(argument_element) for argument_element in self.tree.findall('Argument')]
        self.tag = self.tree.tag
        self.send_trodes_config = self.tree.get('sendTrodesConfig')
        self.module_name = self.tree.get('moduleName')
        self.send_network_info = self.tree.get('sendNetworkInfo')


class Argument:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.flag = self.tree.get('flag')
        self.value = self.tree.get('value')


class GlobalConfiguration:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.headstage_serial = self.tree.get('headstageSerial')
        self.headstage_smart_ref_on = self.tree.get('headstageSmartRefOn')
        self.realtime_mode = self.tree.get('realtimeMode')
        self.headstage_auto_settle_on = self.tree.get('headstageAutoSettleOn')
        self.timestamp_at_creation = self.tree.get('timestampAtCreation')
        self.controller_firmware_version = self.tree.get('controllerFirmwareVersion')
        self.controller_serial = self.tree.get('controllerSerial')
        self.save_displayed_chan_only = self.tree.get('saveDisplayedChanOnly')
        self.headstage_firmware_version = self.tree.get('headstageFirmwareVersion')
        self.qt_version = self.tree.get('qtVersion')
        self.compile_date = self.tree.get('compileDate')
        self.compile_time = self.tree.get('compileTime')
        self.file_prefix = self.tree.get('filePrefix')
        self.headstage_gyro_sensor_on = self.tree.get('headstageGyroSensorOn')
        self.headstage_mag_sensor_on = self.tree.get('headstageMagSensorOn')
        self.trodes_version = self.tree.get('trodesVersion')
        self.headstage_accel_sensor_on = self.tree.get('headstageAccelSensorOn')
        self.commit_head = self.tree.get('commitHead')
        self.system_time_at_creation = self.tree.get('systemTimeAtCreation')
        self.file_path = self.tree.get('filePath')


class HardwareConfiguration:

    def __init__(self, element):
        self.tree = element
        self.devices = [Device(device_element) for device_element in self.tree.findall('Device')]
        self.tag = self.tree.tag
        self.sampling_rate = self.tree.get('samplingRate')
        self.num_channels = self.tree.get('numChannels')


class Device:

    def __init__(self, element):
        self.tree = element
        self.channels = \
            [Channel(channel_element) for channel_element in self.tree.findall('Channel')]
        self.tag = self.tree.tag
        self.name = self.tree.get('name')
        self.num_bytes = self.tree.get('numBytes')
        self.available = self.tree.get('available')
        self.packet_order_preference = self.tree.get('packetOrderPreference')


class Channel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.id = self.tree.get('id')
        self.bit = self.tree.get('bit')
        self.data_type = self.tree.get('dataType')
        self.start_byte = self.tree.get('startByte')
        self.input = self.tree.get('input')


class StreamDisplay:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.background_color = self.tree.get('backgroundColor')
        self.columns = self.tree.get('columns')
        self.pages = self.tree.get('pages')


class AuxDisplayConfiguration:

    def __init__(self, element):
        self.tree = element
        self.disp_channels = [DispChannel(disp_channel_element) for disp_channel_element
                              in self.tree.findall('DispChannel')]
        self.tag = self.tree.tag


class DispChannel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.analyze = self.tree.get('analyze')
        self.id = self.tree.get('id')
        self.device = self.tree.get('device')
        self.color = self.tree.get('color')
        self.max_disp = self.tree.get('maxDisp')


class SpikeConfiguration:

    def __init__(self, element):
        self.tree = element
        self.spike_n_trodes = [SpikeNTrode(spike_n_trode_element) for spike_n_trode_element
                               in self.tree.findall('SpikeNTrode')]
        self.tag = self.tree.tag
        self.categories = self.tree.get('categories')


class SpikeNTrode:

    def __init__(self, element):
        self.tree = element
        self.spike_channels = [SpikeChannel(spike_channel_element) for spike_channel_element
                               in self.tree.findall('SpikeChannel')]
        self.tag = self.tree.tag
        self.low_filter = self.tree.get('lowFilter')
        self.lfp_chan = self.tree.get('LFPChan')
        self.lfp_filter_on = self.tree.get('lfpFilterOn')
        self.ref_group = self.tree.get('refGroup')
        self.group_ref_on = self.tree.get('groupRefOn')
        self.lfp_high_filter = self.tree.get('LFPHighFilter')
        self.hight_filter = self.tree.get('highFilter')
        self.color = self.tree.get('color')
        self.ref_chan = self.tree.get('refChan')
        self.id = self.tree.get('id')
        self.lfp_ref_on = self.tree.get('lfpRefOn')
        self.filter_on = self.tree.get('filterOn')
        self.ref_on = self.tree.get('refOn')
        self.module_data_on = self.tree.get('moduleDataOn')
        self.ref_n_trode_id = self.tree.get('refNTrodeID')


class SpikeChannel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.hw_chan = self.tree.get('hwChan')
        self.max_disp = self.tree.get('maxDisp')
        self.thresh = self.tree.get('thresh')
        self.trigger_on = self.tree.get('triggerOn')
