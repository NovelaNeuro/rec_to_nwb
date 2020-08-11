import numpy as np

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class CameraSampleFrameCountsExtractor:
    def __init__(self, pos_data_path, raw_data_path):
        self.pos_data_path = pos_data_path
        self.raw_data_path = raw_data_path

    def extract_camera_hw_frame_count(self, hw_frame_count_filename):
        content = readTrodesExtractedDataFile(
                  self.pos_data_path + "/" + hw_frame_count_filename + "pos_cameraHWSync"
                  )["data"]
        camera_sample_frame_counts = np.ndarray(shape = (len(content), 2), dtype='uint32')
        for i, record in enumerate(content):
            camera_sample_frame_counts[i, 0] = record[0]
            camera_sample_frame_counts[i, 1] = record[1]
        return camera_sample_frame_counts

    # def extract_timestamps(self, video_timestamps_filename):
    #     # timestamps = readTrodesExtractedDataFile(
    #     #             self.raw_data_path + "/" + video_timestamps_filename + "videoTimeStamps"
    #     #         )["data"]
    #     return timestamps
