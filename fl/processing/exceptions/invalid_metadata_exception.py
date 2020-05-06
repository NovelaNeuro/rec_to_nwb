from fl.processing.exceptions.invalid_exception import InvalidException


class InvalidMetadataException(InvalidException):

    def __str__(self):
        if self.message:
            return 'InvalidMetadataException, {0} '.format(self.message)
        return 'InvalidMetadataException has been thrown!'
