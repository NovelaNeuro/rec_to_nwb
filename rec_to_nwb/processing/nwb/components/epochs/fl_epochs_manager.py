from rec_to_nwb.processing.nwb.components.epochs.epochs_tag_extractor import \
    EpochsTagExtractor
from rec_to_nwb.processing.nwb.components.epochs.fl_epochs_builder import \
    FlEpochsBuilder
from rec_to_nwb.processing.nwb.components.epochs.fl_epochs_extractor import \
    FlEpochsExtractor
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlEpochsManager:

    @beartype
    def __init__(self, datasets: list):
        self.continuous_time_files = [
            dataset.get_continuous_time() for dataset in datasets]
        epochs_tags = self.__get_epochs_tags(datasets)
        self.fl_epochs_builder = FlEpochsBuilder(epochs_tags)

    @staticmethod
    def __get_epochs_tags(datasets):
        epochs_tag_extractor = EpochsTagExtractor(datasets)
        return epochs_tag_extractor.get_tags()

    def get_epochs(self):
        fl_epochs_extractor = FlEpochsExtractor(self.continuous_time_files)
        return self.fl_epochs_builder.build(fl_epochs_extractor.extract_epochs())
