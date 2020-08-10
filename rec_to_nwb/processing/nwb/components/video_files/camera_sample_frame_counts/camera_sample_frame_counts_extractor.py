from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class CameraSampleFrameCountsExtractor:
    def __init__(self, pos_data_path, raw_data_path):
        self.pos_data_path = pos_data_path
        self.raw_data_path = raw_data_path

    def extract_camera_hw_frame_count(self, hw_frame_count_filename):
        timestamps = readTrodesExtractedDataFile(
                    self.pos_data_path + "/" + hw_frame_count_filename + "pos_cameraHWFrameCount.dat"
                )["data"]
        return timestamps

    def extract_timestamps(self, hw_sync_filename):
        timestamps = readTrodesExtractedDataFile(
                    self.raw_data_path + "/" + hw_sync_filename + "videoTimeStamps"
                )["data"]
        return timestamps