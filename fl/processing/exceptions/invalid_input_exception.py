from fldatamigration.processing.exceptions.invalid_exception import InvalidException


class InvalidInputException(InvalidException):

    def __str__(self):
        if self.message:
            return 'InvalidInputException, {0} '.format(self.message)
        return 'InvalidInputException has been thrown!'
