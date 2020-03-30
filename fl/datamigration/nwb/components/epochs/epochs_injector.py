class EpochsInjector:

    @staticmethod
    def inject(fl_epochs, nwb_content):
        for i, tag in enumerate(fl_epochs.tags):
            nwb_content.add_epoch(
                fl_epochs.session_start_times[i],
                fl_epochs.session_end_times[i],
                fl_epochs.tags[i],
            )
        EpochsInjector.__extend_epochs(fl_epochs, nwb_content)

    @staticmethod
    def __extend_epochs(fl_epochs, nwb_content):
        tasks = fl_epochs.tasks
        nwb_content.add_epoch_column('tasks', 'None', data=tasks)
