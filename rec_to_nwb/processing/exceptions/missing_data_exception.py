from rec_to_nwb.processing.exceptions.invalid_exception import InvalidException


class MissingDataException(InvalidException):

    def __str__(self):
        if self.message:
            return 'MissingDataException, {0} '.format(self.message)
        return 'MissingDataException has been thrown!'
