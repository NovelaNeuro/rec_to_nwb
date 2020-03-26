from fl.datamigration.nwb.components.epochs.fl_epochs import FlEpochs


class FlEpochsBuilder:

    @staticmethod
    def build(epochs_extracted_session_times, tags, tasks):
        return FlEpochs(
            epochs_extracted_session_times[0],
            epochs_extracted_session_times[1],
            tags,
            tasks
        )