from fl.datamigration.nwb.components.epochs.epochs_tag_extractor import EpochsTagExtractor
from fl.datamigration.nwb.components.epochs.fl_epochs_builder import FlEpochsBuilder
from fl.datamigration.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor
from fl.datamigration.tools.task_names_extractor import TaskNamesExtractor
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlEpochsManager:

    def __init__(self, datasets, tasks):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(datasets))
        validation_registrator.register(NotNoneValidator(tasks))
        validation_registrator.validate()

        self.continuous_time_files = [dataset.get_continuous_time() for dataset in datasets]
        task_names_extractor = TaskNamesExtractor(tasks)
        epochs_tag_extractor = EpochsTagExtractor(datasets)
        epochs_tags = epochs_tag_extractor.get_tags()
        self.fl_epochs_builder = FlEpochsBuilder(epochs_tags, task_names_extractor.get_task_names())

    def get_epochs(self):
        fl_epochs_extractor = FlEpochsExtractor(self.continuous_time_files)
        return self.fl_epochs_builder.build(fl_epochs_extractor.extract_epochs())
