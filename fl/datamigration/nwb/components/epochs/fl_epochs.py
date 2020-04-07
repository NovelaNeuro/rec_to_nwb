from fl.datamigration.validation.equal_length_validator import EqualLengthValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlEpochs:

    def __init__(self, session_start_times, session_end_times, tags, tasks):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(EqualLengthValidator([session_start_times, session_end_times, tags, tasks]))
        validation_registrator.validate()

        self.session_start_times = session_start_times
        self.session_end_times = session_end_times
        self.tags = tags
        self.tasks = tasks
