from rec_to_nwb.processing.exceptions.invalid_exception import InvalidException


class InvalidHeaderException(InvalidException):

    def __str__(self):
        if self.message:
            return 'InvalidHeaderException, {0} '.format(self.message)
        return 'InvalidHeaderException has been thrown!'
