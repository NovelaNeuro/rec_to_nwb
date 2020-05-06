from fl.datamigration.nwb.components.epochs.epochs_tag_extractor import EpochsTagExtractor
from fl.datamigration.nwb.components.epochs.fl_epochs_builder import FlEpochsBuilder
from fl.datamigration.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlEpochsManager:

    def __init__(self, datasets):
        validate_parameters_not_none(__name__, datasets)

        self.continuous_time_files = [dataset.get_continuous_time() for dataset in datasets]
        epochs_tag_extractor = EpochsTagExtractor(datasets)
        epochs_tags = epochs_tag_extractor.get_tags()
        self.fl_epochs_builder = FlEpochsBuilder(epochs_tags)

    def get_epochs(self):
        fl_epochs_extractor = FlEpochsExtractor(self.continuous_time_files)
        return self.fl_epochs_builder.build(fl_epochs_extractor.extract_epochs())
