from pynwb.device import Device

from ndx_fllab_novela.header_device import HeaderDevice
from ndx_fllab_novela.probe import Probe

from lf.datamigration.tools.validate_input_parameters import validate_input_parameters


class DeviceFactory:

    @classmethod
    def create_device(cls, lf_device):
        validate_input_parameters(__name__, lf_device)
        validate_input_parameters(__name__, lf_device.name)
        return Device(
            name=str(lf_device.name)
        )

    @classmethod
    def create_probe(cls, lf_probe):
        validate_input_parameters(__name__, lf_probe)
        validate_input_parameters(__name__, lf_probe.probe_id, lf_probe.metadata)
        return Probe(
            probe_type=lf_probe.metadata['probe_type'],
            contact_size=lf_probe.metadata['contact_size'],
            num_shanks=lf_probe.metadata['num_shanks'],
            contact_side_numbering=lf_probe.metadata['contact_side_numbering'],
            id=lf_probe.probe_id,
            name=str(lf_probe.probe_id)
        )

    @classmethod
    def create_header_device(cls, lf_header_device):
        validate_input_parameters(__name__, lf_header_device)
        validate_input_parameters(__name__, lf_header_device.name, lf_header_device.global_configuration)

        return HeaderDevice(
            name=lf_header_device.name,
            headstage_serial=lf_header_device.global_configuration.headstage_serial,
            headstage_smart_ref_on=lf_header_device.global_configuration.headstage_smart_ref_on,
            realtime_mode=lf_header_device.global_configuration.realtime_mode,
            headstage_auto_settle_on=lf_header_device.global_configuration.headstage_auto_settle_on,
            timestamp_at_creation=lf_header_device.global_configuration.timestamp_at_creation,
            controller_firmware_version=lf_header_device.global_configuration.controller_firmware_version,
            controller_serial=lf_header_device.global_configuration.controller_serial,
            save_displayed_chan_only=lf_header_device.global_configuration.save_displayed_chan_only,
            headstage_firmware_version=lf_header_device.global_configuration.headstage_firmware_version,
            qt_version=lf_header_device.global_configuration.qt_version,
            compile_date=lf_header_device.global_configuration.compile_date,
            compile_time=lf_header_device.global_configuration.compile_time,
            file_prefix=lf_header_device.global_configuration.file_prefix,
            headstage_gyro_sensor_on=lf_header_device.global_configuration.headstage_gyro_sensor_on,
            headstage_mag_sensor_on=lf_header_device.global_configuration.headstage_mag_sensor_on,
            trodes_version=lf_header_device.global_configuration.trodes_version,
            headstage_accel_sensor_on=lf_header_device.global_configuration.headstage_accel_sensor_on,
            commit_head=lf_header_device.global_configuration.commit_head,
            system_time_at_creation=lf_header_device.global_configuration.system_time_at_creation,
            file_path=lf_header_device.global_configuration.file_path
        )
