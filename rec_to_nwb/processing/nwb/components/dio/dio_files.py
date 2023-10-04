import glob
import os


class DioFiles:
    def __init__(self, directories, dio_metadata):
        self.directories = directories
        self.dio_metadata = dio_metadata

    def get_files(self):
        multiple_datasets_dio_files = [
            self.__get_dict(dataset) for dataset in self.directories
        ]
        filtered_datasets_dio_files = self.__filter_files(
            multiple_datasets_dio_files, self.dio_metadata
        )
        return filtered_datasets_dio_files

    @classmethod
    def __filter_files(cls, multiple_datasets_dio_files, dio_metadata):
        return [
            {
                dio_file: single_dataset[dio_file]
                for dio_file in single_dataset
                if dio_file in [dio_event["description"] for dio_event in dio_metadata]
            }
            for single_dataset in multiple_datasets_dio_files
        ]

    @classmethod
    def __get_dict(cls, directory):
        dio_dict = {}
        for file in glob.glob(os.path.join(directory, "*.dat")):
            if file.split(".")[-2].split("_")[-2] == "MCU":
                # To avoid this warning, remove MCU_IO data from being displayed via the .trodesconf, this will stop MCU_IO extraction
                print(
                    f"WARNING: MCU_IO data are not currently handled by rec_to_nwb. Skipping file: {file}."
                )
                # TODO: find MCU_IO binaries if they exist and appropriately insert these data into nwbs in future version of rec_to_nwb
            elif file.split(".")[-2].split("_")[-2] == "Controller":
                print(
                    f"WARNING: Controller_IO data are not currently handled by rec_to_nwb. Skipping file: {file}."
                )
            else:
                if not(file.split(".")[-2].split("_")[-2] == "ECU"):
                 print(
                    f"WARNING: {file.split('.')[-2].split('_')[-2]} is not a recognized dio type. Including file: {file}, but proceed with caution."
                )   
                dio_name = file.split(".")[-2].split("_")[
                    -1
                ]  # This string should be of the form "Din12" "Dout5"
                dio_dict[dio_name] = os.path.join(directory, file)
        return dio_dict
