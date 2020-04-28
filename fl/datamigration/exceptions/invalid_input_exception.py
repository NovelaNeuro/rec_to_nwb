from fl.datamigration.exceptions.invalid_exception import InvalidException


class InvalidInputException(InvalidException):

    def __str__(self):
        if self.message:
            return 'InvalidInputException, {0} '.format(self.message)
        else:
            return 'InvalidInputException has been thrown!'
