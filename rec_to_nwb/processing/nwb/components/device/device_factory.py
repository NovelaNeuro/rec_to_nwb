from ndx_franklab_novela.header_device import HeaderDevice
from ndx_franklab_novela.probe import Probe
from pynwb.device import Device

from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class DeviceFactory:

    @classmethod
    def create_device(cls, fl_device):
        validate_parameters_not_none(__name__, fl_device)
        validate_parameters_not_none(__name__, fl_device.name)
        return Device(
            name=str(fl_device.name)
        )

    @classmethod
    def create_probe(cls, fl_probe):
        validate_parameters_not_none(__name__, fl_probe)
        validate_parameters_not_none(__name__, fl_probe.probe_id, fl_probe.metadata)
        probe = Probe(
            id=fl_probe.probe_id,
            name="probe " + str(fl_probe.probe_id),
            probe_type=fl_probe.metadata['probe_type'],
            units=fl_probe.metadata['units'],
            probe_description=fl_probe.metadata['probe_description'],
            num_shanks=len(fl_probe.shanks),
            contact_side_numbering=fl_probe.metadata['contact_side_numbering'],
            contact_size=fl_probe.metadata['contact_size'],
        )
        for shank in fl_probe.shanks:
            probe.add_shank(shank)

        return probe

    @classmethod
    def create_header_device(cls, fl_header_device):
        validate_parameters_not_none(__name__, fl_header_device)
        validate_parameters_not_none(__name__, fl_header_device.name, fl_header_device.global_configuration)

        return HeaderDevice(
            name=fl_header_device.name,
            headstage_serial=fl_header_device.global_configuration.headstage_serial,
            headstage_smart_ref_on=fl_header_device.global_configuration.headstage_smart_ref_on,
            realtime_mode=fl_header_device.global_configuration.realtime_mode,
            headstage_auto_settle_on=fl_header_device.global_configuration.headstage_auto_settle_on,
            timestamp_at_creation=fl_header_device.global_configuration.timestamp_at_creation,
            controller_firmware_version=fl_header_device.global_configuration.controller_firmware_version,
            controller_serial=fl_header_device.global_configuration.controller_serial,
            save_displayed_chan_only=fl_header_device.global_configuration.save_displayed_chan_only,
            headstage_firmware_version=fl_header_device.global_configuration.headstage_firmware_version,
            qt_version=fl_header_device.global_configuration.qt_version,
            compile_date=fl_header_device.global_configuration.compile_date,
            compile_time=fl_header_device.global_configuration.compile_time,
            file_prefix=fl_header_device.global_configuration.file_prefix,
            headstage_gyro_sensor_on=fl_header_device.global_configuration.headstage_gyro_sensor_on,
            headstage_mag_sensor_on=fl_header_device.global_configuration.headstage_mag_sensor_on,
            trodes_version=fl_header_device.global_configuration.trodes_version,
            headstage_accel_sensor_on=fl_header_device.global_configuration.headstage_accel_sensor_on,
            commit_head=fl_header_device.global_configuration.commit_head,
            system_time_at_creation=fl_header_device.global_configuration.system_time_at_creation,
            file_path=fl_header_device.global_configuration.file_path
        )
