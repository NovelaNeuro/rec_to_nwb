from rec_to_nwb.processing.exceptions.invalid_exception import InvalidException


class InvalidPathException(InvalidException):

    def __str__(self):
        if self.message:
            return 'InvalidPathException, {0} '.format(self.message)
        return 'InvalidPathException has been thrown!'
