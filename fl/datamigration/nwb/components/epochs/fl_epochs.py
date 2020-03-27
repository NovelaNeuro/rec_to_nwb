from fl.datamigration.tools.validate_parameters import validate_parameters_equal_length


class FlEpochs:

    def __init__(self, session_start_times, session_end_times, tags, tasks):
        validate_parameters_equal_length(__name__, session_start_times, session_end_times, tags, tasks)

        self.session_start_times = session_start_times
        self.session_end_times = session_end_times
        self.tags = tags
        self.tasks = tasks
