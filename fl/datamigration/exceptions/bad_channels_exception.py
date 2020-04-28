from fl.datamigration.exceptions.invalid_exception import InvalidException


class CorruptedDataException(InvalidException):

    def __str__(self):
        if self.message:
            return 'CorruptedDataException, {0} '.format(self.message)
        else:
            return 'CorruptedDataException has been thrown!'
