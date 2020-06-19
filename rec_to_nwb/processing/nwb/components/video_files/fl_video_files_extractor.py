from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class FlVideoFilesExtractor:

    def __init__(self, raw_data_path, video_directory, video_files_metadata):
        self.raw_data_path = raw_data_path
        self.video_directory = video_directory
        self.video_files_metadata = video_files_metadata

    def extract_video_files(self):
        video_files = self.video_files_metadata
        extracted_video_files = []
        for video_file in video_files:
            new_fl_video_file = {
                "name": video_file["name"],
                "timestamps": readTrodesExtractedDataFile(
                    self.raw_data_path + "/"
                    + video_file["name"][:-4]
                    + "videoTimeStamps.cameraHWSync"
                )["data"],
                "device": video_file["camera_id"]
            }
            extracted_video_files.append(new_fl_video_file)
