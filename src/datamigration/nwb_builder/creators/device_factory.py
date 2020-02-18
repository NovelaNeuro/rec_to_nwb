from pynwb.device import Device

from ndx_franklab_novela.header_device import HeaderDevice
from ndx_franklab_novela.probe import Probe


class DeviceFactory:

    @classmethod
    def create_device(cls,device_name):
        return Device(
            name=str(device_name)
        )

    @classmethod
    def create_probe(cls,probe_metadata, probe_id):
        return Probe(
                probe_type=probe_metadata['probe_type'],
                contact_size=probe_metadata['contact_size'],
                num_shanks=probe_metadata['num_shanks'],
                id=probe_id,
                name=str(probe_id)
            )

    @classmethod
    def create_header_device(cls,global_configuration, name):
        return HeaderDevice(
                            name=name,
                            headstage_serial=global_configuration.headstage_serial,
                            headstage_smart_ref_on=global_configuration.headstage_smart_ref_on,
                            realtime_mode=global_configuration.realtime_mode,
                            headstage_auto_settle_on=global_configuration.headstage_auto_settle_on,
                            timestamp_at_creation=global_configuration.timestamp_at_creation,
                            controller_firmware_version=global_configuration.controller_firmware_version,
                            controller_serial=global_configuration.controller_serial,
                            save_displayed_chan_only=global_configuration.save_displayed_chan_only,
                            headstage_firmware_version=global_configuration.headstage_firmware_version,
                            qt_version=global_configuration.qt_version,
                            compile_date=global_configuration.compile_date,
                            compile_time=global_configuration.compile_time,
                            file_prefix=global_configuration.file_prefix,
                            headstage_gyro_sensor_on=global_configuration.headstage_gyro_sensor_on,
                            headstage_mag_sensor_on=global_configuration.headstage_mag_sensor_on,
                            trodes_version=global_configuration.trodes_version,
                            headstage_accel_sensor_on=global_configuration.headstage_accel_sensor_on,
                            commit_head=global_configuration.commit_head,
                            system_time_at_creation=global_configuration.system_time_at_creation,
                            file_path=global_configuration.file_path
                            )