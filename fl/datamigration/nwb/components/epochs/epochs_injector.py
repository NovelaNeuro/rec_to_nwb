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
        if len(nwb_content.epochs) < len(fl_epochs.tasks):
            tasks = fl_epochs.tasks[0:len(nwb_content.epochs)]
        else:
            tasks = fl_epochs.tasks
        nwb_content.add_epoch_column('tasks', '-', data=tasks)
