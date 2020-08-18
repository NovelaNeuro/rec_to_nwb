class FlHeaderDevice:

    def __init__(self, name, global_configuration_dict):
        self.name = name
        name = name,
        headstage_serial = global_configuration_dict['headstage_serial']
        headstage_smart_ref_on = global_configuration_dict['headstage_smart_ref_on']
        realtime_mode = global_configuration_dict['realtime_mode']
        headstage_auto_settle_on = global_configuration_dict['headstage_auto_settle_on']
        timestamp_at_creation = global_configuration_dict['timestamp_at_creation']
        controller_firmware_version = global_configuration_dict['controller_firmware_version']
        controller_serial = global_configuration_dict['controller_serial']
        save_displayed_chan_only = global_configuration_dict['save_displayed_chan_only']
        headstage_firmware_version = global_configuration_dict['headstage_firmware_version']
        qt_version = global_configuration_dict['qt_version']
        compile_date = global_configuration_dict['compile_date']
        compile_time = global_configuration_dict['compile_time']
        file_prefix = global_configuration_dict['file_prefix']
        headstage_gyro_sensor_on = global_configuration_dict['headstage_gyro_sensor_on']
        headstage_mag_sensor_on = global_configuration_dict['headstage_mag_sensor_on']
        trodes_version = global_configuration_dict['trodes_version']
        headstage_accel_sensor_on = global_configuration_dict['headstage_accel_sensor_on']
        commit_head = global_configuration_dict['commit_head']
        system_time_at_creation = global_configuration_dict['system_time_at_creation']
        file_path = global_configuration_dict['file_path']

