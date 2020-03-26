from fl.datamigration.nwb.components.epochs.fl_epochs_creator import FlEpochsCreator
from fl.datamigration.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor


class FlEpochsManager:

    def __init__(self, continuous_time_files, epoch_tags, metadata):
        self.fl_epochs_extractor = FlEpochsExtractor(continuous_time_files)
        self.epoch_tags = epoch_tags
        self.metadata = metadata

    def get_epochs(self):
        return FlEpochsCreator.create(
            self.fl_epochs_extractor.extract_epochs(),
            self.epoch_tags,
            self.__get_tasks_from_metadata
        )

    def __get_tasks_from_metadata(self):
        return [task_dict['task_name'] for task_dict in self.metadata.tasks]

