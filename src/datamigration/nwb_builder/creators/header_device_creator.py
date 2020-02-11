from src.datamigration.extension.header_device import HeaderDevice


class HeaderDeviceCreator:

    @staticmethod
    def create_header_device(header, name):
        header_fields = header.configuration.global_configuration
        return HeaderDevice(
                            name=name,
                            headstage_serial=header_fields.headstage_serial,
                            headstage_smart_ref_on=header_fields.headstage_smart_ref_on,
                            realtime_mode=header_fields.realtime_mode,
                            headstage_auto_settle_on=header_fields.headstage_auto_settle_on,
                            timestamp_at_creation=header_fields.timestamp_at_creation,
                            controller_firmware_version=header_fields.controller_firmware_version,
                            controller_serial=header_fields.controller_serial,
                            save_displayed_chan_only=header_fields.save_displayed_chan_only,
                            headstage_firmware_version=header_fields.headstage_firmware_version,
                            qt_version=header_fields.qt_version,
                            compile_date=header_fields.compile_date,
                            compile_time=header_fields.compile_time,
                            file_prefix=header_fields.file_prefix,
                            headstage_gyro_sensor_on=header_fields.headstage_gyro_sensor_on,
                            headstage_mag_sensor_on=header_fields.headstage_mag_sensor_on,
                            trodes_version=header_fields.trodes_version,
                            headstage_accel_sensor_on=header_fields.headstage_accel_sensor_on,
                            commit_head=header_fields.commit_head,
                            system_time_at_creation=header_fields.system_time_at_creation,
                            file_path=header_fields.file_path
                            )