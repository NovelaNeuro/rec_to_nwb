from fl.datamigration.nwb.components.epochs.epochs_tag_extractor import EpochsTagExtractor
from fl.datamigration.nwb.components.epochs.fl_epochs_builder import FlEpochsBuilder
from fl.datamigration.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor
from fl.datamigration.tools.task_names_extractor import TaskNamesExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlEpochsManager:

    def __init__(self, datasets, metadata):
        validate_parameters_not_none(__name__, datasets, metadata)

        self.continuous_time_files = [dataset.get_continuous_time() for dataset in datasets]
        self.task_names_extractor = TaskNamesExtractor(metadata)
        epochs_tag_extractor = EpochsTagExtractor(datasets)
        self.epochs_tags = epochs_tag_extractor.get_tags()

    def get_epochs(self):
        fl_epochs_extractor = FlEpochsExtractor(self.continuous_time_files)
        return FlEpochsBuilder.build(
            fl_epochs_extractor.extract_epochs(),
            self.epochs_tags,
            self.task_names_extractor.get_task_names()
        )
