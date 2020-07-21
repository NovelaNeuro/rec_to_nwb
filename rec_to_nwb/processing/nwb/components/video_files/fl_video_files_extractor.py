import numpy as np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlVideoFilesExtractor:

    @beartype
    def __init__(self, raw_data_path: str, video_files_metadata: list):
        self.raw_data_path = raw_data_path
        self.video_files_metadata = video_files_metadata

    def extract_video_files(self):
        video_files = self.video_files_metadata
        extracted_video_files = []
        for video_file in video_files:
            new_fl_video_file = {
                "name": video_file["name"],
                "timestamps": self.convert_timestamps(readTrodesExtractedDataFile(
                    self.raw_data_path + "/"
                    + video_file["name"][:-4]
                    + "videoTimeStamps.cameraHWSync"
                )["data"]),
                "device": video_file["camera_id"]
            }
            extracted_video_files.append(new_fl_video_file)
        return extracted_video_files

    def convert_timestamps(self, timestamps):
        converted_timestamps = np.ndarray(shape=np.shape(timestamps), dtype='float64')
        for i, record in enumerate(timestamps):
            converted_timestamps[i] = record[2]/1E9
        return converted_timestamps
