from fl.datamigration.nwb.components.epochs.epochs_tag_extractor import EpochsTagExtractor
from fl.datamigration.nwb.components.epochs.fl_epochs_builder import FlEpochsBuilder
from fl.datamigration.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor
from fl.datamigration.tools.name_extractor import NameExtractor
from fl.datamigration.tools.task_names_extractor import TaskNamesExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlEpochsManager:

    def __init__(self, datasets, tasks):
        validate_parameters_not_none(
            class_name=__name__,
            args=[datasets, tasks],
            args_name=[NameExtractor.extract_name(self.__init__)[1],
                       NameExtractor.extract_name(self.__init__)[2]]
        )
        self.continuous_time_files = [dataset.get_continuous_time() for dataset in datasets]
        task_names_extractor = TaskNamesExtractor(tasks)
        epochs_tag_extractor = EpochsTagExtractor(datasets)
        epochs_tags = epochs_tag_extractor.get_tags()
        self.fl_epochs_builder = FlEpochsBuilder(epochs_tags, task_names_extractor.get_task_names())

    def get_epochs(self):
        fl_epochs_extractor = FlEpochsExtractor(self.continuous_time_files)
        return self.fl_epochs_builder.build(fl_epochs_extractor.extract_epochs())
