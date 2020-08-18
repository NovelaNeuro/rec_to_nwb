from rec_to_nwb.processing.nwb.components.device.header.fl_header_device_builder import FlHeaderDeviceBuilder


class FlHeaderDeviceManager:

    def __init__(self, name, global_configuration, default_configuration):
        self.name = name
        self.global_configuration = global_configuration
        self.default_global_configuration = default_configuration

    def get_fl_header_device(self):
        return FlHeaderDeviceBuilder.build(self.name, self.__compare_global_configuration_with_default())

    def __compare_global_configuration_with_default(self):
        global_configuration_dict = self.global_configuration.__dict__
        default_configuration_dict = self.__get_default_global_configuration()
        for single_key in default_configuration_dict:
            if single_key in global_configuration_dict.keys():
                global_configuration_dict[single_key] = default_configuration_dict[single_key]
        return global_configuration_dict

    def __get_default_global_configuration(self):
        global_configuration_dict = {}
        global_configuration_dict['headstage_serial'] = self.default_global_configuration.headstage_serial,
        global_configuration_dict['headstage_smart_ref_on'] = self.default_global_configuration.headstage_smart_ref_on,
        global_configuration_dict['realtime_mode'] = self.default_global_configuration.realtime_mode,
        global_configuration_dict['headstage_auto_settle_on'] = self.default_global_configuration.headstage_auto_settle_on,
        global_configuration_dict['timestamp_at_creation'] = self.default_global_configuration.timestamp_at_creation,
        global_configuration_dict['controller_firmware_version'] = self.default_global_configuration.controller_firmware_version,
        global_configuration_dict['controller_serial'] = self.default_global_configuration.controller_serial,
        global_configuration_dict['save_displayed_chan_only'] = self.default_global_configuration.save_displayed_chan_only,
        global_configuration_dict['headstage_firmware_version'] = self.default_global_configuration.headstage_firmware_version,
        global_configuration_dict['qt_version'] = self.default_global_configuration.qt_version,
        global_configuration_dict['compile_date'] = self.default_global_configuration.compile_date,
        global_configuration_dict['compile_time'] = self.default_global_configuration.compile_time,
        global_configuration_dict['file_prefix'] = self.default_global_configuration.file_prefix,
        global_configuration_dict['headstage_gyro_sensor_on'] = self.default_global_configuration.headstage_gyro_sensor_on,
        global_configuration_dict['headstage_mag_sensor_on'] = self.default_global_configuration.headstage_mag_sensor_on,
        global_configuration_dict['trodes_version'] = self.default_global_configuration.trodes_version,
        global_configuration_dict['headstage_accel_sensor_on'] = self.default_global_configuration.headstage_accel_sensor_on,
        global_configuration_dict['commit_head'] = self.default_global_configuration.commit_head,
        global_configuration_dict['system_time_at_creation'] = self.default_global_configuration.system_time_at_creation,
        global_configuration_dict['file_path'] = self.default_global_configuration.file_path
        return global_configuration_dict
