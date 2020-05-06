from fldatamigration.processing.exceptions.invalid_metadata_exception import InvalidMetadataException
from fldatamigration.processing.validation.task_validation_summary import TaskValidationSummary
from fldatamigration.processing.validation.validator import Validator


class TaskValidator(Validator):

    def __init__(self, tasks):
        self.tasks = tasks

    def create_summary(self):
        if len(self.tasks) == 0:
            raise InvalidMetadataException("There are no tasks defined in metadata.yml file.")
        return TaskValidationSummary(self.tasks)
