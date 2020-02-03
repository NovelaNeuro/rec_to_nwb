import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


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