class EpochsInjector:

    def __init__(self, fl_epochs, nwb_content):
        self.fl_epochs = fl_epochs
        self.nwb_content = nwb_content

    def inject(self):
        for i in range(len(self.fl_epochs.tags)):
            self.nwb_content.add_epoch(
                self.fl_epochs.session_start_times[i],
                self.fl_epochs.session_end_times[i],
                self.fl_epochs.tags[i],
            )
        self.__extend_epochs()

    def __extend_epochs(self):
        self.nwb_content.add_epoch_column('tasks', '-', data=self.fl_epochs.tasks)
