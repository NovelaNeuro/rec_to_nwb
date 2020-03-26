from fl.datamigration.nwb.components.epochs.fl_epochs_builder import FlEpochsBuilder
from fl.datamigration.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor


class FlEpochsManager:

    def __init__(self, continuous_time_files, datasets, metadata):
        self.continuous_time_files = continuous_time_files
        self.epoch_tags = [dataset.name for dataset in datasets]
        self.metadata = metadata

    def get_epochs(self):
        return FlEpochsBuilder.build(
            FlEpochsExtractor.extract_epochs(self.continuous_time_files),
            self.epoch_tags,
            self.__get_tasks_from_metadata()
        )

    def __get_tasks_from_metadata(self):
        return [task_dict['task_name'] for task_dict in self.metadata['tasks']]

