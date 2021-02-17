import re

from rec_to_nwb.processing.exceptions.invalid_metadata_exception import InvalidMetadataException
from rec_to_nwb.processing.nwb.components.position.fl_position_builder import FlPositionBuilder
from rec_to_nwb.processing.nwb.components.position.fl_position_extractor import FlPositionExtractor
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_equal_length


class FlPositionManager:

    @beartype
    def __init__(self, datasets: list, metadata: dict, dataset_names: list,
                    process_timestamps: bool,
                    convert_timestamps: bool = True):
        self.datasets = datasets
        self.metadata = metadata
        self.dataset_names = dataset_names
        self.process_timestamps = process_timestamps

        self.fl_position_extractor = FlPositionExtractor(datasets,
                                        convert_timestamps=convert_timestamps)
        self.fl_position_builder = FlPositionBuilder()

    @beartype
    def get_fl_positions(self) -> list:
        cameras_ids = self.__get_cameras_ids(self.dataset_names, self.metadata)
        meters_per_pixels = self.__get_meters_per_pixels(cameras_ids, self.metadata)

        position_datas = self.fl_position_extractor.get_positions()
        columns_labels = self.fl_position_extractor.get_columns_labels()
        if self.process_timestamps:
            timestamps = self.fl_position_extractor.get_timestamps()

            validate_parameters_equal_length(__name__, position_datas, columns_labels, timestamps)

            return [
                self.fl_position_builder.build(
                    position_data=position_data,
                    column_labels=column_labels,
                    timestamps=timestamp,
                    conversion=float(meters_per_pixel)
                )
                for position_data, column_labels, timestamp, meters_per_pixel in
                zip(position_datas, columns_labels, timestamps, meters_per_pixels)
            ]
        else:
            validate_parameters_equal_length(__name__, position_datas, columns_labels)

            return [
                self.fl_position_builder.build(
                    position_data=position_data,
                    column_labels=column_labels,
                    timestamps=[],
                    conversion=float(meters_per_pixel)
                )
                for position_data, column_labels, meters_per_pixel in
                zip(position_datas, columns_labels, meters_per_pixels)
            ]





    @staticmethod
    def __get_cameras_ids(dataset_names, metadata):
        camera_ids = []
        for dataset_name in dataset_names:
            # extract the first the first element of the dataset_name as the epoch number
            dataset_elements = str(dataset_name).split('_')
            epoch_num = str(int(dataset_elements[0]))
            try:
                camera_ids.append(
                    next(
                        task['camera_id']
                        for task in metadata['tasks']
                        if epoch_num in task['task_epochs']
                    )[0]
                )
            except:
                raise InvalidMetadataException('Invalid camera metadata for datasets')
        return camera_ids

    @staticmethod
    def __get_meters_per_pixels(cameras_ids, metadata):
        meters_per_pixels = []
        for camera_id in cameras_ids:
            try:
                meters_per_pixels.append(
                    next(
                        float(camera['meters_per_pixel'])
                        for camera in metadata['cameras']
                        if camera_id == camera['id']
                    )
                )
            except:
                raise InvalidMetadataException('Invalid camera metadata')
        return meters_per_pixels
